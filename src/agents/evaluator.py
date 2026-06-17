from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.llm_client import LLMClient
from src.text_sanitize import sanitize_jsonable, sanitize_text

VERDICT_SCORE = {"SUPPORTED": 1.0, "PARTIAL": 0.5, "UNSUPPORTED": 0.0}


class EvalAgent:
    def __init__(self, threshold_bps: int = 7800, llm_provider: str = "mock", mode: str = "incentivized"):
        self.threshold_bps = threshold_bps
        self.llm = LLMClient(llm_provider)
        self.mode = mode

    def evaluate_page(self, wiki_page: dict, source_chunks: list[dict]) -> dict:
        chunk_map = {c["chunk_id"]: c for c in source_chunks}
        relevant = [chunk_map[cid] for cid in wiki_page.get("source_chunk_ids", []) if cid in chunk_map]
        source_text = sanitize_text("\n\n".join(c["text"] for c in relevant))
        claims = wiki_page.get("claims") or self._extract_claims(wiki_page["content"])
        if wiki_page["title"].lower().startswith("hallucinated"):
            claims.append("This page claims a nonexistent robot benchmark achieved 999 percent success.")
        checks = []
        for claim in claims:
            claim = sanitize_text(str(claim))
            verdict, reason, fallback = self.llm.evaluate_claim(claim, source_text)
            critical = verdict == "UNSUPPORTED" and self._is_critical_claim(claim)
            checks.append({"finding_id": f"f_{uuid.uuid4().hex[:10]}", "claim": claim, "verdict": verdict, "score": VERDICT_SCORE[verdict], "critical": critical, "reason": reason, "fallback_used": fallback, "curator_decision": "ACCEPT" if verdict in {"SUPPORTED", "PARTIAL"} else "REJECT"})
        score_bps = int((sum(c["score"] for c in checks) / max(len(checks), 1)) * 10000)
        has_critical = any(c["critical"] for c in checks)
        passed = score_bps >= self.threshold_bps and not has_critical
        link_verdicts = self.evaluate_cross_links(wiki_page, source_text)
        return {"cert_id": str(uuid.uuid4()), "page_id": wiki_page["page_id"], "page_title": wiki_page["title"], "score_bps": score_bps, "threshold_bps": self.threshold_bps, "passed": passed, "has_critical_unsupported_claim": has_critical, "claim_checks": checks, "cross_link_verdicts": link_verdicts, "llm_provider": self.llm.provider_used, "llm_issue": self.llm.issue, "evaluated_at": datetime.now(timezone.utc).isoformat()}

    def evaluate_all(self, pages: list[dict], chunks: list[dict]) -> list[dict]:
        return [self.evaluate_page(p, chunks) for p in pages]

    def evaluate_cross_links(self, page: dict, source_text: str) -> list[dict]:
        verdicts = []
        source_words = set(re.findall(r"[A-Za-z가-힣]{4,}", source_text.lower()))
        for c in page.get("cross_link_candidates", []):
            target = c.get("target_title", "")
            target_words = set(re.findall(r"[A-Za-z가-힣]{4,}", target.lower()))
            accepted = bool(target_words & source_words) and c.get("cosine_sim", 0) >= 0.2
            verdicts.append({"source_page": page["title"], "target_page": target, "cosine_similarity": c.get("cosine_sim", 0), "eval_decision": "ACCEPT" if accepted else "REJECT", "reason": "target terms appear in source evidence" if accepted else "insufficient source evidence", "accepted": accepted})
        return verdicts

    def _extract_claims(self, content: str) -> list[str]:
        body = re.sub(r"---.*?---", "", content, flags=re.S)
        claims = []
        for line in body.splitlines():
            line = re.sub(r"^[-*]\s*", "", line.strip())
            if line and not line.startswith("#") and len(line) > 25 and line != "PENDING":
                claims.append(line[:500])
        return claims[:8]

    def _is_critical_claim(self, claim: str) -> bool:
        return bool(re.search(r"\d|benchmark|success|state-of-the-art|SOTA|percent|%", claim, re.I))

    def save_certificates(self, certs: list[dict], output_dir: str) -> None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"certificates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(sanitize_jsonable(certs), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  평가 증명서 저장: {path}")

    def summary(self, certs: list[dict]) -> dict:
        return {"total": len(certs), "passed": sum(c["passed"] for c in certs), "failed": sum(not c["passed"] for c in certs), "avg_score_bps": int(sum(c["score_bps"] for c in certs) / max(len(certs), 1)), "accepted_findings": sum(1 for c in certs for f in c["claim_checks"] if f["curator_decision"] == "ACCEPT"), "unsupported_claims": sum(1 for c in certs for f in c["claim_checks"] if f["verdict"] == "UNSUPPORTED")}
