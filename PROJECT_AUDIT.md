# Project Audit

Date: 2026-06-04
Workspace: `/home/cheon/Documents/workspace/ai_blockchain`
Git status: not a git repository, so no branch could be created. No destructive changes were made during this audit.

## Repository Structure Read

Important paths inspected:

- `src/main.py` - primary CLI entry point.
- `demo/demo_pipeline.py` - demo runner used for repeatable daily runs.
- `src/pipeline/runner.py` - agentic pipeline orchestration.
- `src/agents/curator.py` - wiki page generation agent.
- `src/agents/evaluator.py` - source-groundedness evaluator.
- `src/agents/payer.py` - mock/optional payment agent.
- `src/llm_client.py` - mock/Ollama/OpenAI provider abstraction.
- `contracts/PageCertificateRegistry.sol` - certificate-only smart contract surface.
- `usage_log/USAGE_LOG.md` and `usage_log/RUN_LOG.jsonl` - usage/run evidence.
- `obsidian_vault/` - generated Obsidian research vault.
- `PRESENTATION_DEMO.html` - presentation dashboard.

## Main Entry Points

Reviewer-facing commands:

```bash
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider mock --mock-chain --mock-payment --append-usage-log
python demo/build_obsidian_vault.py
./demo/open_obsidian_vault.sh
```

Application-style CLI:

```bash
python -m src.main --sources data/sources --output output/wiki --threshold-bps 7800 --llm-provider mock --mock-chain --mock-payment --append-usage-log
```

## What Already Works

- PDF sources are loaded from `data/sources/` and chunked.
- Obsidian Markdown pages are generated under `output/wiki/`.
- `obsidian_vault/` is generated with `Home.md`, daily logs, topic page, paper pages, and evidence files.
- `EvalAgent` assigns `score_bps` and PASS/FAIL decisions.
- Failed pages remain local-only and do not receive certificate transactions.
- Mock certificate tx hashes use `0xmock_cert_`.
- Mock payment tx hashes use `0xmock_pay_` and reward accepted EvalAgent findings.
- Usage evidence exists for multiple runs, including latest `run_20260604_121901` with 107 PDFs, 1306 chunks, 108 pages, PASS 106, FAIL 2.
- Presentation dashboard and project reports exist.
- `basedpyright` currently reports 0 errors / 0 warnings for project configuration.

## What Is Mock/Demo Only

- Blockchain certification is mock unless real WorldLand environment variables are configured and integration is extended.
- WLC payment is mock unless real payment integration is explicitly added and approved.
- Latest recorded run requested `ollama`, used `eval_provider_requested: mock` for the large run, and recorded `llm_provider_used: mock+ollama` with fallback disclosed.
- `Hallucinated_Failure_Fixture` is an intentional local-only fail page used to demonstrate the publication gate.

## External Services and Integrations

Implemented/available:

- Local filesystem: PDF input, Markdown output, usage logs, Obsidian vault.
- Local Ollama: supported by `--llm-provider ollama`; server must be running.
- OpenAI Responses API: supported by `--llm-provider openai` with `OPENAI_API_KEY`.
- WorldLand contract/payment: optional future integration, currently mock for demo safety.
- Obsidian AppImage: installed locally for Graph View demonstration.

Not implemented:

- GitHub issue/PR automation.
- Messaging interfaces such as Slack/Telegram.
- Real MCP server runtime.
- Real WorldLand transaction or real WLC transfer.

## LLM, API Key, Tool, Database, File, Web, GitHub, Messaging Findings

- LLM calls: `src/llm_client.py` supports `mock`, `ollama`, and `openai` providers.
- API keys: `OPENAI_API_KEY` is read from environment only; no real key found.
- File operations: project-bounded path resolution exists in `src/main.py`; pipeline reads `data/sources/`, writes `output/wiki/`, `usage_log/`, `evidence/`, and `obsidian_vault/`.
- Web requests: OpenAI and Ollama endpoints can be called when selected; no hidden web fetch in mock mode.
- Database: none.
- GitHub integration: none.
- Messaging interface: none.
- Tool-like modules: chunker, curator, evaluator, payer, mock chain, vault builder; a formal lightweight tool layer is recommended.

## Log Production

Current log artifacts:

- `usage_log/USAGE_LOG.md` - human-readable usage entries.
- `usage_log/RUN_LOG.jsonl` - structured run summaries.
- `usage_log/CERTIFICATE_LOG.md` - latest certificate log.
- `usage_log/EVALUATION_LOG.md` - latest evaluation log.
- `usage_log/PAYMENT_LOG.md` - latest payment log.
- `obsidian_vault/Daily Logs/` - accumulated daily research pages.

## Security Risks and Boundaries

Positive controls:

- `.gitignore` ignores `.env`, `.env.*`, key/pem/secret/wallet patterns, and `.sisyphus/`.
- `.env.example` contains placeholders only.
- `src/main.py` rejects source/output paths outside the project root.
- Failed pages are local-only and do not trigger mock certificate transactions.
- Real payment is blocked unless explicit non-mock mode and credentials are provided.

Risks / gaps:

- This workspace is not a git repo, so git-history secret scanning is not possible here.
- `.env.example` has been aligned to current runtime environment variables; CLI defaults such as `--mock-chain`, `--mock-payment`, and `--threshold-bps` remain argparse flags rather than env defaults.
- `demo/build_obsidian_vault.py` deletes/recreates only project-local `obsidian_vault/`; safe as written, but should not be repointed outside the repo.
- Retrieved PDFs are untrusted text and must not be allowed to instruct tool behavior.
- Real WorldLand/WLC integration requires explicit human approval before any transaction/payment.

## Project Classification

Best classification: **Research Productivity Agent** with a **Blockchain Agent** trust/evidence layer.

Reason: the daily workflow is reading AI papers across major fields, creating an Obsidian research vault, checking source-groundedness, logging usage, and optionally recording certificates/rewards.

## Immediate Recommendations

1. Keep the implementation structure; do not rewrite from scratch.
2. Update final docs around the Research Productivity Agent identity.
3. Add required course docs under `docs/`, `paper/`, `slides/`, and `demo_video/`.
4. Keep `.env.example` aligned if new runtime variables are added.
5. Keep the documented tool layer in `docs/tool_architecture.md` aligned with code changes.
6. Keep all real blockchain/payment/API actions gated by environment variables and human approval.
