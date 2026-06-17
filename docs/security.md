# Security Checklist

## Credential Handling

- [x] No real API keys committed intentionally.
- [x] `.env` and `.env.*` ignored by `.gitignore`.
- [x] `.env.example` contains placeholders only.
- [x] OpenAI credentials are loaded from `OPENAI_API_KEY`.
- [x] WorldLand network values are expected from environment variables; wallet secrets must not be committed.
- [x] Real private keys must never be printed.

## Filesystem Boundaries

- [x] `src/main.py` restricts CLI source/output paths to the project root.
- [x] Default source path is `data/sources/`.
- [x] Default wiki output path is `output/wiki/`.
- [x] Obsidian vault builder deletes/recreates only project-local `obsidian_vault/`.
- [ ] If future MCP filesystem server is added, configure sandbox root to this repository only.

## External Text and Prompt Injection

- [x] PDFs are treated as untrusted source text.
- [x] The agent should not follow instructions found inside papers or fetched documents.
- [x] Generated claims are checked against source chunks.
- [x] Unsupported critical claims fail local-only.

## Write / Send / Pay / Publish Actions

- [x] Local Markdown/log writes are expected and project-local.
- [x] Failed pages do not create certificate tx records.
- [x] Mock payment uses `0xmock_pay_` hashes only.
- [x] Real payment must require explicit confirmation every time.
- [x] Real blockchain publication must require explicit confirmation and MetaMask/funded-wallet approval.

## Network and API Boundaries

- [x] Mock mode performs no external LLM call.
- [x] Ollama mode calls local `OLLAMA_BASE_URL` only.
- [x] OpenAI mode requires `OPENAI_API_KEY`; missing key falls back to mock.
- [ ] New external domains require first-use confirmation before future integration.

## Logging Strategy

- [x] Usage logs are stored in `usage_log/USAGE_LOG.md`.
- [x] Structured run logs are stored in `usage_log/RUN_LOG.jsonl`.
- [x] Certificate/evaluation/payment logs are stored separately.
- [x] Failures and fallback behavior are recorded honestly.
- [x] Certificate payload export does not submit transactions or print private keys.
