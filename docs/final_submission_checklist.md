# Final Submission Checklist

This checklist maps the project to the course-style AI agent + blockchain requirements.

## Implemented

- User interface: CLI accepts natural-language requests through `python -m src.main "오늘 새 논문 요약해줘" --dry-run --channel cli --user cheon`.
- LLM/local model: `mock`, `ollama`, and `openai` providers are supported; the latest large evidence run requested Ollama and used mock evaluation for runtime.
- Agent role/instructions: README, workflow, security, and paper docs define the Research Productivity Agent role and safety limits.
- External tools/data: PDF parser, wiki curator, evaluator, Obsidian builder, mock certificate registry, certificate payload exporter, and read-only blockchain RPC helpers are implemented.
- Workflow loop: Goal -> Input -> Tools -> Check -> Record -> Human Review -> Output is implemented and documented.
- Usage logs: `usage_log/USAGE_LOG.md` and `usage_log/RUN_LOG.jsonl` exist.
- Tool-call logs: `usage_log/TOOL_CALL_LOG.jsonl` records channel, task type, tool, status, latency, and args summary.
- Verifier/check: `EvalAgent` uses `score_bps`, `threshold_bps`, and `FAIL_LOCAL_ONLY` gate behavior.
- Human approval: real payment, real blockchain publication, OpenAI on sensitive PDFs, and external writes require explicit approval.
- MCP: `mcp_servers/research_vault_agent.py` exposes `search_project_memory`, `export_certificate_payloads`, and `blockchain_read` over stdio JSON-RPC.
- Blockchain read tool: `src/blockchain/read_tools.py` supports config/latest block/balance/transaction reads without private keys.
- Blockchain certificate preparation: `demo/export_certificate_payloads.py` exports `certifyPage` payloads without submitting transactions.

## User Must Do Before Submission

- Run or collect truthful usage entries across the required number of days. Do not fabricate future logs.
- If showing real WorldLand interaction, create a dedicated test MetaMask wallet, add the course-provided network settings, request faucet funds, deploy `PageCertificateRegistry` in Remix, and only then submit a small exported payload with explicit approval.
- Fill `.env` only locally if using RPC/MetaMask-related values; never commit `.env` or private keys.
- Initialize or copy this workspace into a GitHub repository before final submission, because the current workspace is not a git repository.
- Open Obsidian with `./demo/open_obsidian_vault.sh` and verify Graph View visually before presentation.

## Safe Demo Commands

```bash
python -m src.main "오늘 새 논문 요약해줘" --dry-run --channel cli --user cheon
python demo/export_certificate_payloads.py --limit 3
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_servers/research_vault_agent.py
```
