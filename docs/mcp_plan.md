# MCP Plan

This project keeps integrations small. The implementation has local modules for reading PDFs, generating notes, evaluating claims, logging runs, building an Obsidian vault, exporting certificate payloads, and reading blockchain RPC state. A minimal custom MCP-style stdio server is implemented at `mcp_servers/research_vault_agent.py` so these capabilities can be demonstrated as discoverable tools while preserving approval boundaries.

## MCP Principle

MCP server is not the model. MCP server is a tool provider. The host application controls model choice, tool discovery, credentials, workspace roots, and approval policy.

## Free / Low-Cost MCP Servers

1. **filesystem** — read and write files only inside this repository, useful for `data/sources/`, `output/wiki/`, `usage_log/`, and `obsidian_vault/`.
2. **fetch** — retrieve public paper pages or documentation when the user explicitly asks to import a public source.
3. **memory or sqlite** — store structured daily run summaries, preferences, and recurring research topics.

Optional future server:

4. **github** — create issues for failed evaluations or final-submission tasks, scoped to one repository and requiring write approval.

## Implemented Custom MCP Server

Server name: `research_vault_agent`

Purpose: expose the project-specific paper-to-Obsidian workflow as safe tools.

### Tool 1: `search_project_memory(query: str, limit: int = 5) -> list[dict]`

- **Purpose:** Search daily logs, run summaries, and generated note titles.
- **Input schema:** `query` string, `limit` integer 1-20.
- **Output schema:** list of `{source: str, title: str, excerpt: str, path: str}`.
- **Side effects:** none.
- **Approval requirement:** none if restricted to project root.
- **Expected failure modes:** no matches, missing log files, unreadable file.

### Tool 2: `summarize_new_item(path: str, provider: str = "mock") -> dict`

- **Purpose:** Summarize one user-added PDF or Markdown source and return draft note metadata.
- **Input schema:** `path` inside `data/sources/`, provider `mock|ollama|openai`.
- **Output schema:** `{title: str, summary: str, key_claims: list[str], source_chunks: list[str], provider_used: str}`.
- **Side effects:** none by default; draft only.
- **Approval requirement:** required before using `openai` provider because it may send text externally and incur cost.
- **Expected failure modes:** file outside sandbox, unsupported extension, LLM unavailable, extraction failure.

### Tool 3: `write_usage_log(date: str, task: str, outcome: str, latency_ms: int, cost_estimate: float = 0.0) -> dict`

- **Purpose:** Append a real usage entry after a run.
- **Input schema:** date ISO string, task, outcome, latency in ms, cost estimate.
- **Output schema:** `{ok: bool, path: str, entry_id: str}`.
- **Side effects:** appends to `usage_log/USAGE_LOG.md` and/or `usage_log/RUN_LOG.jsonl`.
- **Approval requirement:** no approval for project-local log writes; user confirmation if editing historical entries.
- **Expected failure modes:** permission error, malformed date, log path missing.

### Tool 4: `verify_output(page_path: str, threshold_bps: int = 7800) -> dict`

- **Purpose:** Re-check a generated page against source chunks.
- **Input schema:** page path inside `output/wiki/` or `obsidian_vault/Pages/`, threshold basis points.
- **Output schema:** `{score_bps: int, passed: bool, unsupported_claims: list[str], critical: bool}`.
- **Side effects:** none unless caller separately records result.
- **Approval requirement:** none.
- **Expected failure modes:** missing metadata, source chunk not found, invalid threshold.

### Tool 5: `estimate_cost(input_tokens: int, output_tokens: int, model: str) -> dict`

- **Purpose:** Estimate cost before using external OpenAI calls.
- **Input schema:** input token estimate, output token estimate, model name.
- **Output schema:** `{model: str, estimated_cost_usd: float, warning: str}`.
- **Side effects:** none.
- **Approval requirement:** none.
- **Expected failure modes:** unknown model pricing, invalid token counts.

## Threat Model by Server

| Server | Data Access | Write? | Credentials | Approval Policy | Sandbox | Logging |
|---|---|---:|---|---|---|---|
| filesystem | project files only | yes | none | writes require path inside repo | repository root | every write logged |
| fetch | public URLs | no by default | none | first-use domain confirmation | no local write unless approved | URL and timestamp logged |
| memory/sqlite | run summaries and preferences | yes | none | append allowed, edits require confirmation | project-local DB | every mutation logged |
| github | one repo metadata/issues | optional | repo-scoped token | write actions require confirmation | one configured repo | issue/PR actions logged |
| custom `research_vault_agent` | sources, wiki, logs, evidence | yes for log/vault tools | optional OpenAI key | external LLM/write/pay/publish require confirmation | repository root | tool call log and outcome |

## Approval Rules

- Read-only project search: auto-allowed.
- Draft summaries: auto-allowed for mock/local Ollama; approval for OpenAI.
- Local log append: allowed.
- Historical log edit: approval required.
- Real blockchain certificate: approval required.
- Real WLC payment: approval required every time.
- External URL fetch: first-use domain confirmation.

## Failure Handling

- If an LLM provider is unavailable, fallback to deterministic mock and record the fallback.
- If a tool tries to access a path outside the sandbox, reject and log the attempt.
- If a write fails, do not retry destructively; report the exact file and error.
- If output verification fails, keep the page local-only.

## Smoke Test

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_servers/research_vault_agent.py
```
