from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
JsonDict = dict[str, object]


@dataclass(frozen=True)
class CliArgs:
    summary: Path | None
    output: Path
    evaluator_address: str
    limit: int


def latest_summary_path() -> Path:
    summaries = sorted((ROOT / "evidence").glob("run_*_summary.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not summaries:
        raise RuntimeError("No evidence/run_*_summary.json file found. Run demo_pipeline first.")
    for summary in summaries:
        data = cast(JsonDict, json.loads(summary.read_text(encoding="utf-8")))
        records = data.get("chain_records", [])
        if isinstance(records, list) and records:
            return summary
    raise RuntimeError("No summary with certificate chain_records found. Run a PASS-producing demo first.")




def resolve_evidence_path(value: Path) -> Path:
    base = (ROOT / "evidence").resolve()
    candidate = (ROOT / value).resolve() if not value.is_absolute() else value.resolve()
    if not candidate.is_relative_to(base):
        raise ValueError(f"Path outside evidence directory is not allowed: {candidate}")
    return candidate

def load_json(path: Path) -> JsonDict:
    return cast(JsonDict, json.loads(path.read_text(encoding="utf-8")))


def str_field(data: JsonDict, key: str) -> str:
    return str(data[key])


def int_field(data: JsonDict, key: str) -> int:
    value = data[key]
    if isinstance(value, int):
        return value
    return int(str(value))


def page_content_by_id() -> dict[str, str]:
    pages: dict[str, str] = {}
    for meta_path in (ROOT / "output" / "wiki").glob("*.meta.json"):
        meta = load_json(meta_path)
        page_id = str(meta.get("page_id", ""))
        page_path = meta_path.with_name(meta_path.name.removesuffix(".meta.json") + ".md")
        if page_id and page_path.exists():
            pages[page_id] = page_path.read_text(encoding="utf-8")
    return pages


def bytes32_hex(value: str) -> str:
    cleaned = value.removeprefix("0x")
    if len(cleaned) == 64 and all(c in "0123456789abcdefABCDEF" for c in cleaned):
        return "0x" + cleaned.lower()
    return "0x" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_payloads(summary: JsonDict, evaluator_address: str) -> list[JsonDict]:
    page_contents = page_content_by_id()
    payloads: list[JsonDict] = []
    records_obj = summary.get("chain_records", [])
    if not isinstance(records_obj, list):
        return payloads
    records = cast(list[object], records_obj)
    for item in records:
        if not isinstance(item, dict):
            continue
        record = cast(JsonDict, item)
        page_id = str_field(record, "page_id")
        if page_id not in page_contents:
            raise RuntimeError(f"Missing markdown content for certified page_id: {page_id}")
        page_hash = hashlib.sha256(page_contents[page_id].encode("utf-8")).hexdigest()
        payloads.append({
            "page_title": str_field(record, "page_title"),
            "mock_tx_hash": str_field(record, "tx_hash"),
            "certifyPage_args": {
                "pageId": page_id,
                "pageHash": "0x" + page_hash,
                "certHash": bytes32_hex(str_field(record, "cert_hash")),
                "scoreBps": int_field(record, "score_bps"),
                "thresholdBps": int_field(record, "threshold_bps"),
                "evaluator": evaluator_address,
            },
        })
    return payloads


def parse_args(argv: list[str] | None = None) -> CliArgs:
    tokens = list(sys.argv[1:] if argv is None else argv)
    summary: Path | None = None
    output = ROOT / "evidence" / "certificate_payloads_latest.json"
    evaluator_address = "0x0000000000000000000000000000000000000001"
    limit = 0
    index = 0
    while index < len(tokens):
        flag = tokens[index]
        if flag in {"--summary", "--output", "--evaluator-address", "--limit"}:
            if index + 1 >= len(tokens):
                raise SystemExit(f"Missing value for {flag}")
            value = tokens[index + 1]
            if flag == "--summary":
                summary = Path(value)
            elif flag == "--output":
                output = Path(value)
            elif flag == "--evaluator-address":
                evaluator_address = value
            else:
                limit = int(value)
            index += 2
            continue
        if flag in {"-h", "--help"}:
            print("Usage: python demo/export_certificate_payloads.py [--summary PATH] [--output PATH] [--evaluator-address ADDRESS] [--limit N]")
            raise SystemExit(0)
        raise SystemExit(f"Unknown argument: {flag}")
    return CliArgs(summary=summary, output=output, evaluator_address=evaluator_address, limit=limit)

def main() -> None:
    args = parse_args()
    try:
        summary_path = resolve_evidence_path(args.summary) if args.summary else latest_summary_path()
        output_path = resolve_evidence_path(args.output)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    summary = load_json(summary_path)
    payloads = build_payloads(summary, args.evaluator_address)
    if args.limit > 0:
        payloads = payloads[: args.limit]
    export: JsonDict = {
        "run_id": summary.get("run_id"),
        "source_summary": str(summary_path.relative_to(ROOT)),
        "contract": "PageCertificateRegistry.certifyPage",
        "note": "Prepared payloads only. Submit through MetaMask/Remix after explicit approval and funded test wallet.",
        "payload_count": len(payloads),
        "payloads": payloads,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _ = output_path.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output_path), "run_id": export["run_id"], "payload_count": len(payloads)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
