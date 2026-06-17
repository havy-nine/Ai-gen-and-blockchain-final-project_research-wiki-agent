from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.blockchain.read_tools import get_balance, get_latest_block, get_transaction, network_config
from src.tool_log import append_tool_call
from src.text_sanitize import sanitize_jsonable

from src.pipeline.runner import PipelineRunner


def resolve_project_path(base: Path, value: str) -> Path:
    candidate = (base / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    if not candidate.is_relative_to(base):
        raise ValueError(f"Path outside project root is not allowed: {candidate}")
    return candidate


def infer_task_type(request: str) -> str:
    lowered = request.lower()
    if any(word in lowered for word in ["block", "wallet", "tx", "transaction", "balance", "chain", "metamask"]):
        return "blockchain_read"
    if any(word in lowered for word in ["요약", "summary", "paper", "논문"]):
        return "summarize_papers"
    return "agent_run"


def run_blockchain_read(task_type: str, request: str) -> dict[str, object]:
    if "balance" in request.lower():
        words = [w.strip(",. ") for w in request.split()]
        address = next((w for w in words if w.startswith("0x") and len(w) == 42), "")
        if address:
            return get_balance(address)
    if "tx" in request.lower() or "transaction" in request.lower():
        words = [w.strip(",. ") for w in request.split()]
        tx_hash = next((w for w in words if w.startswith("0x") and len(w) == 66), "")
        if tx_hash:
            return get_transaction(tx_hash)
    if task_type == "blockchain_read":
        return get_latest_block()
    return network_config()


def main() -> None:
    parser = argparse.ArgumentParser(description="WorldLand Knowledge Wiki Agent")
    parser.add_argument("request", nargs="?", default="", help="Natural-language user request for the agent interface")
    parser.add_argument("--sources", default="data/sources")
    parser.add_argument("--output", default="output/wiki")
    parser.add_argument("--threshold-bps", type=int, default=7800)
    parser.add_argument("--llm-provider", choices=["mock", "ollama", "openai"], default="ollama")
    parser.add_argument("--mock-chain", dest="mock_chain", action="store_true", default=True)
    parser.add_argument("--real-chain", dest="mock_chain", action="store_false")
    parser.add_argument("--mock-payment", dest="mock_payment", action="store_true", default=True)
    parser.add_argument("--real-payment", dest="mock_payment", action="store_false")
    parser.add_argument("--append-usage-log", action="store_true")
    parser.add_argument("--eval-provider", choices=["mock", "ollama", "openai"], default=None)
    parser.add_argument("--channel", default="cli")
    parser.add_argument("--user", default="local-user")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent.parent
    task_type = infer_task_type(str(args.request))
    if args.dry_run:
        blockchain_status = run_blockchain_read(task_type, str(args.request))
        result = {"request": args.request, "channel": args.channel, "user_identity": args.user, "task_type": task_type, "would_run_pipeline": task_type != "blockchain_read", "blockchain_status": blockchain_status}
        append_tool_call("agent_request_interface", "dry_run", 0, args.channel, task_type, str(args.request), "request accepted", args.user)
        print(json.dumps(sanitize_jsonable(result), ensure_ascii=False, indent=2))
        return
    if task_type == "blockchain_read":
        blockchain_result = run_blockchain_read(task_type, str(args.request))
        append_tool_call("blockchain_read", "success", 0, args.channel, task_type, str(args.request), "read-only result", args.user)
        print(json.dumps(sanitize_jsonable(blockchain_result), ensure_ascii=False, indent=2))
        return
    try:
        sources_dir = resolve_project_path(base, args.sources)
        output_dir = resolve_project_path(base, args.output)
    except ValueError as exc:
        parser.error(str(exc))
    append_tool_call("agent_request_interface", "start", 0, args.channel, task_type, str(args.request), "pipeline starting", args.user)
    PipelineRunner(sources_dir=str(sources_dir), output_dir=str(output_dir), threshold_bps=args.threshold_bps, llm_provider=args.llm_provider, mock_chain=args.mock_chain, mock_payment=args.mock_payment, append_usage_log=args.append_usage_log, eval_provider=args.eval_provider).run()


if __name__ == "__main__":
    main()
