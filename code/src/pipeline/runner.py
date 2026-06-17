from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from src.agents.curator import WikiCuratorAgent
from src.agents.evaluator import EvalAgent
from src.agents.payer import PayAgent
from src.blockchain.contract import WorldLandCertificateRegistry
from src.blockchain.mock_chain import MockBlockchain
from src.pipeline.chunker import load_and_chunk_sources
from src.tool_log import logged_tool
from src.text_sanitize import sanitize_jsonable


class PipelineRunner:
    def __init__(self, sources_dir: str = "data/sources", output_dir: str = "output/wiki", threshold_bps: int = 7800, llm_provider: str = "ollama", mock_chain: bool = True, mock_payment: bool = True, append_usage_log: bool = False, eval_provider: str | None = None):
        self.sources_dir = sources_dir
        self.output_dir = output_dir
        self.threshold_bps = threshold_bps
        self.llm_provider = llm_provider
        self.mock_chain = mock_chain
        self.mock_payment = mock_payment
        self.append_usage_log = append_usage_log
        self.eval_provider = eval_provider or llm_provider
        self.run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")

    def run(self) -> dict:
        print(f"=== WorldLand Knowledge Wiki Agent 실행 ({self.run_id}) ===")
        with logged_tool("load_and_chunk_sources", args_summary=self.sources_dir):
            chunks = load_and_chunk_sources(self.sources_dir)
        input_source_files = len({c["source_file"] for c in chunks})
        input_chunks = len(chunks)
        curator = WikiCuratorAgent(llm_provider=self.llm_provider)
        with logged_tool("WikiCuratorAgent.generate_wiki_pages", args_summary=f"chunks={len(chunks)}"):
            pages = curator.generate_wiki_pages(chunks)
        self._inject_fail_fixture_if_needed(pages, chunks)
        evaluator = EvalAgent(threshold_bps=self.threshold_bps, llm_provider=self.eval_provider)
        with logged_tool("EvalAgent.evaluate_all", args_summary=f"pages={len(pages)} chunks={len(chunks)}"):
            certs = evaluator.evaluate_all(pages, chunks)
        if all(c["passed"] for c in certs):
            self._inject_fail_fixture_if_needed(pages, chunks, force=True)
            with logged_tool("EvalAgent.evaluate_all", args_summary=f"pages={len(pages)} chunks={len(chunks)} force_fixture=true"):
                certs = evaluator.evaluate_all(pages, chunks)
        by_page = {c["page_id"]: c for c in certs}
        for page in pages:
            curator.apply_accepted_links(page, by_page[page["page_id"]].get("cross_link_verdicts", []))
            page["content"] = page["content"].replace("PENDING_EVAL", "PASS" if by_page[page["page_id"]]["passed"] else "FAIL_LOCAL_ONLY")
        with logged_tool("WikiCuratorAgent.save_wiki_pages", args_summary=self.output_dir):
            curator.save_wiki_pages(pages, self.output_dir)
        with logged_tool("CertificateRegistry.certify_passed_pages", args_summary=f"mock_chain={self.mock_chain}"):
            chain_records = self._certify_passed_pages(pages, certs)
        with logged_tool("PayAgent.reward_accepted_findings", args_summary=f"mock_payment={self.mock_payment}"):
            payments = PayAgent(mock_payment=self.mock_payment).reward_accepted_findings(certs)
        result = {"run_id": self.run_id, "timestamp": datetime.now(timezone.utc).isoformat(), "threshold_bps": self.threshold_bps, "llm_provider_requested": self.llm_provider, "eval_provider_requested": self.eval_provider, "llm_provider_used": self._provider_used(certs, pages), "fallback_message": self._fallback_message(certs, pages), "source_files": input_source_files, "chunks": input_chunks, "fixture_chunks": len(chunks) - input_chunks, "pages": len(pages), "passed": sum(c["passed"] for c in certs), "failed": sum(not c["passed"] for c in certs), "certificates_on_chain": len(chain_records), "payments": len(payments), "certs": certs, "chain_records": chain_records, "payments_detail": payments}
        self._write_logs(result)
        print(f"PASS {result['passed']} / FAIL {result['failed']} / cert tx {len(chain_records)} / payment tx {len(payments)}")
        return result

    def _certify_passed_pages(self, pages: list[dict], certs: list[dict]) -> list[dict]:
        chain = MockBlockchain() if self.mock_chain else WorldLandCertificateRegistry()
        page_map = {p["page_id"]: p for p in pages}
        records = []
        for cert in certs:
            if not cert["passed"]:
                continue
            records.append(chain.certify_page(page_map[cert["page_id"]], cert))
        return records

    def _inject_fail_fixture_if_needed(self, pages: list[dict], chunks: list[dict], force: bool = False) -> None:
        if not force and any(p["title"].lower().startswith("hallucinated") for p in pages):
            return
        chunk_id = "hallucinated_fixture_chunk"
        chunks.append({"chunk_id": chunk_id, "source_file": "hallucinated_test_fixture.txt", "source_type": "fixture", "text": "This fixture intentionally contains no support for the hallucinated benchmark claim.", "start_line": 1, "end_line": 1, "token_count": 20})
        pages.append({"page_id": "hallucinated_fixture_page", "title": "Hallucinated Failure Fixture", "content": "# Hallucinated Failure Fixture\n\n## Summary\nIntentional unsupported test page.\n\n## Key Claims\n- This page claims a nonexistent robot benchmark achieved 999 percent success.\n\n## Source Evidence\n- No supporting source evidence.\n\n## Cross-link Candidates\n- None\n\n## Verification Status\nPENDING_EVAL\n", "source_chunk_ids": [chunk_id], "source_file": "hallucinated_test_fixture.txt", "claims": ["This page claims a nonexistent robot benchmark achieved 999 percent success."], "cross_link_candidates": [], "accepted_cross_links": [], "llm_provider": "mock", "llm_fallback_used": False, "llm_issue": "", "created_at": datetime.now(timezone.utc).isoformat()})

    def _provider_used(self, certs: list[dict], pages: list[dict]) -> str:
        providers = {c.get("llm_provider", "mock") for c in certs} | {p.get("llm_provider", "mock") for p in pages}
        return "+".join(sorted(providers))

    def _fallback_message(self, certs: list[dict], pages: list[dict]) -> str:
        issues = [c.get("llm_issue", "") for c in certs if c.get("llm_issue")] + [p.get("llm_issue", "") for p in pages if p.get("llm_issue")]
        return issues[0] if issues else ""

    def _write_logs(self, result: dict) -> None:
        usage = Path("usage_log")
        evidence = Path("evidence")
        usage.mkdir(exist_ok=True)
        evidence.mkdir(exist_ok=True)
        self._append_jsonl(usage / "RUN_LOG.jsonl", self._compact(result))
        self._write_md_logs(usage, result)
        (evidence / f"{self.run_id}_summary.json").write_text(json.dumps(sanitize_jsonable(self._compact(result)), ensure_ascii=False, indent=2), encoding="utf-8")

    def _write_md_logs(self, usage: Path, result: dict) -> None:
        if self.append_usage_log:
            with (usage / "USAGE_LOG.md").open("a", encoding="utf-8") as f:
                f.write(f"\n## {result['run_id']}\n")
                f.write(f"- timestamp: {result['timestamp']}\n- source_files: {result['source_files']}\n- chunks: {result['chunks']}\n- pages: {result['pages']}\n- threshold_bps: {result['threshold_bps']}\n- pass: {result['passed']}\n- fail: {result['failed']}\n- llm_provider_used: {result['llm_provider_used']}\n")
                if result["fallback_message"]:
                    f.write(f"- note: {result['fallback_message']}\n")
        cert_lines = ["# Certificate Log", ""]
        chain_by_page = {r["page_id"]: r for r in result["chain_records"]}
        for c in result["certs"]:
            if c["passed"]:
                r = chain_by_page[c["page_id"]]
                cert_lines.append(f"- CERTIFIED | {r['tx_hash']} | {r['page_title']} | score_bps={r['score_bps']} threshold_bps={r['threshold_bps']}")
            else:
                cert_lines.append(f"- SKIP_CHAIN | tx_hash=None | {c['page_title']} | score_bps={c['score_bps']} threshold_bps={c['threshold_bps']} critical={c['has_critical_unsupported_claim']}")
        (usage / "CERTIFICATE_LOG.md").write_text("\n".join(cert_lines) + "\n", encoding="utf-8")
        eval_lines = ["# Evaluation Log", ""]
        for c in result["certs"]:
            eval_lines.append(f"- {'PASS' if c['passed'] else 'FAIL_LOCAL_ONLY'} | {c['page_title']} | score_bps={c['score_bps']} threshold_bps={c['threshold_bps']} critical={c['has_critical_unsupported_claim']} chain_action={'CERTIFY' if c['passed'] else 'SKIP_CHAIN'}")
        (usage / "EVALUATION_LOG.md").write_text("\n".join(eval_lines) + "\n", encoding="utf-8")
        pay_lines = ["# Payment Log", ""]
        for p in result["payments_detail"]:
            pay_lines.append(f"- {p['tx_hash']} | finding={p['finding_id']} | page={p['page_title']} | amount_wlc={p['amount_wlc']}")
        (usage / "PAYMENT_LOG.md").write_text("\n".join(pay_lines) + "\n", encoding="utf-8")

    def _append_jsonl(self, path: Path, data: dict) -> None:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(sanitize_jsonable(data), ensure_ascii=False) + "\n")

    def _compact(self, result: dict) -> dict:
        return {k: v for k, v in result.items() if k not in {"certs", "payments_detail"}}
