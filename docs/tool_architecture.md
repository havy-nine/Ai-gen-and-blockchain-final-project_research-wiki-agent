# Tool Architecture

The project uses a small Python tool layer rather than many unused integrations. Core tools are regular Python modules, and `mcp_servers/research_vault_agent.py` exposes the safest project-specific tools through a minimal MCP-style stdio JSON-RPC server.

## Current Tools

| Tool/module | Type | Purpose | Read/write | Approval |
|---|---|---|---|---|
| `load_and_chunk_sources` in `src/pipeline/chunker.py` | read-only data tool | Read PDFs/Markdown/text and produce chunks | read `data/sources/` | no extra approval |
| `WikiCuratorAgent` in `src/agents/curator.py` | project-specific custom tool | Generate Obsidian Markdown pages | writes via runner to `output/wiki/` | local write allowed |
| `EvalAgent` in `src/agents/evaluator.py` | verification tool | Check claims and assign PASS/FAIL in bps | read source chunks | no extra approval |
| `PayAgent` in `src/agents/payer.py` | reward/logging tool | Reward accepted findings with mock payment records | writes logs through runner | real payment requires approval |
| `MockBlockchain` in `src/blockchain/mock_chain.py` | mock external-action tool | Create certificate-like mock tx records for PASS pages | local records only | real chain requires approval |
| `src/blockchain/read_tools.py` | read-only blockchain tool | Check network config, latest block, balance, or transaction through EVM RPC | read-only network call if RPC is configured | no private key required |
| `demo/export_certificate_payloads.py` | blockchain preparation tool | Export `certifyPage` payloads for PASS pages | writes `evidence/certificate_payloads_latest.json` | no transaction; MetaMask approval required later |
| `mcp_servers/research_vault_agent.py` | custom MCP server | Expose project memory search, certificate payload export, and blockchain read tools | stdio JSON-RPC | write/export tools remain local; real tx not supported |
| `PipelineRunner` in `src/pipeline/runner.py` | orchestrator | Goal -> Input -> Tools -> Check -> Record -> Output | reads/writes project files | external actions gated |
| `demo/build_obsidian_vault.py` | memory/output builder | Build Obsidian vault and cumulative daily pages | recreates project-local `obsidian_vault/` | local write allowed |

## Minimum Useful Tool Set Mapping

- Read-only data tool: `load_and_chunk_sources`.
- Project-specific custom tool: `WikiCuratorAgent` + `EvalAgent` workflow.
- Logging/memory tool: `PipelineRunner._write_logs`, `src/tool_log.py`, and `demo/build_obsidian_vault.py`.

## Tool Call Boundaries

- Tools operate inside the project workspace by default.
- `src/main.py` rejects source/output paths outside the project root.
- External LLM calls occur only when `--llm-provider ollama` or `--llm-provider openai` is selected.
- Missing LLM provider falls back to deterministic mock and logs the fallback.
- Real payment and real blockchain publication are not part of the default demo. `demo/export_certificate_payloads.py` prepares transaction arguments only and never submits them. `src/blockchain/read_tools.py` is read-only and never uses a private key.

## Human Approval

Required before:

- real WorldLand certificate submission after reviewing exported payloads,
- real WLC transfer,
- OpenAI use on sensitive PDFs,
- historical log edits,
- writes outside the project root,
- GitHub issue/PR creation if added later.
