from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import cast
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.blockchain.read_tools import get_balance, get_latest_block, get_transaction, network_config
from src.tool_log import append_tool_call
JsonDict = dict[str, object]
TOOLS: list[JsonDict] = [
    {
        "name": "search_project_memory",
        "description": "Search generated notes, daily logs, and run summaries inside this project.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 5}}, "required": ["query"]},
    },
    {
        "name": "export_certificate_payloads",
        "description": "Return path and count for prepared PageCertificateRegistry.certifyPage payloads. Does not submit transactions.",
        "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer", "default": 3}}},
    },
    {
        "name": "blockchain_read",
        "description": "Read-only EVM/WorldLand RPC helper for network config, latest block, balance, or transaction lookup.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "enum": ["config", "latest_block", "balance", "transaction"]}, "address": {"type": "string"}, "tx_hash": {"type": "string"}}, "required": ["action"]},
    },
]
def content_response(data: object) -> JsonDict:
    return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=2)}]}
def search_project_memory(args: JsonDict) -> JsonDict:
    query = str(args.get("query", "")).lower()
    limit_obj = args.get("limit", 5)
    limit = int(limit_obj) if isinstance(limit_obj, int | str) else 5
    results: list[JsonDict] = []
    for base in [ROOT / "obsidian_vault", ROOT / "usage_log", ROOT / "evidence"]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if query in text.lower() or query in path.name.lower():
                results.append({"path": str(path.relative_to(ROOT)), "excerpt": text[:280].replace("\n", " ")})
                if len(results) >= limit:
                    return content_response(results)
    return content_response(results)
def export_certificate_payloads(args: JsonDict) -> JsonDict:
    limit_obj = args.get("limit", 3)
    limit = int(limit_obj) if isinstance(limit_obj, int | str) else 3
    from demo.export_certificate_payloads import build_payloads, latest_summary_path, load_json
    summary_path = latest_summary_path()
    summary = load_json(summary_path)
    payloads = build_payloads(summary, "0x0000000000000000000000000000000000000001")[:limit]
    output = ROOT / "evidence" / "certificate_payloads_latest.json"
    export = {"run_id": summary.get("run_id"), "source_summary": str(summary_path.relative_to(ROOT)), "payload_count": len(payloads), "payloads": payloads, "note": "payload-only; no transaction submitted"}
    output.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    return content_response({"output": str(output.relative_to(ROOT)), "payload_count": len(payloads), "transaction_submitted": False})
def blockchain_read(args: JsonDict) -> JsonDict:
    action = str(args.get("action", "config"))
    if action == "latest_block":
        data = get_latest_block()
    elif action == "balance":
        data = get_balance(str(args.get("address", "")))
    elif action == "transaction":
        data = get_transaction(str(args.get("tx_hash", "")))
    else:
        data = network_config()
    return content_response(data)
def call_tool(name: str, args: JsonDict) -> JsonDict:
    if name == "search_project_memory":
        return search_project_memory(args)
    if name == "export_certificate_payloads":
        return export_certificate_payloads(args)
    if name == "blockchain_read":
        return blockchain_read(args)
    raise ValueError(f"Unknown tool: {name}")
def handle(request: JsonDict) -> JsonDict:
    method = str(request.get("method", ""))
    request_id = request.get("id")
    if method == "initialize":
        result: JsonDict = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "research_vault_agent", "version": "1.0.0"}}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = cast(JsonDict, request.get("params", {}))
        name = str(params.get("name", ""))
        args = cast(JsonDict, params.get("arguments", {}))
        result = call_tool(name, args)
        append_tool_call(f"mcp.{name}", "success", 0, "mcp", "tool_call", json.dumps(args, ensure_ascii=False), "ok")
    else:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}
    return {"jsonrpc": "2.0", "id": request_id, "result": result}
def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = handle(cast(JsonDict, json.loads(line)))
        except Exception as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": exc.__class__.__name__, "data": str(exc)}}
        print(json.dumps(response, ensure_ascii=False), flush=True)
if __name__ == "__main__":
    main()
