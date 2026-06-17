from __future__ import annotations

import json
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL_LOG = ROOT / "usage_log" / "TOOL_CALL_LOG.jsonl"


def append_tool_call(
    tool: str,
    status: str,
    latency_ms: int,
    channel: str = "cli",
    task_type: str = "agent_run",
    args_summary: str = "",
    result_summary: str = "",
    user_identity: str = "local-user",
) -> None:
    TOOL_LOG.parent.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_identity": user_identity,
        "channel": channel,
        "task_type": task_type,
        "tool": tool,
        "args_summary": args_summary,
        "status": status,
        "latency_ms": latency_ms,
        "result_summary": result_summary,
    }
    with TOOL_LOG.open("a", encoding="utf-8") as handle:
        _ = handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


@contextmanager
def logged_tool(
    tool: str,
    channel: str = "cli",
    task_type: str = "agent_run",
    args_summary: str = "",
    user_identity: str = "local-user",
) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    except Exception as exc:
        append_tool_call(tool, "error", int((time.perf_counter() - start) * 1000), channel, task_type, args_summary, exc.__class__.__name__, user_identity)
        raise
    append_tool_call(tool, "success", int((time.perf_counter() - start) * 1000), channel, task_type, args_summary, "ok", user_identity)
