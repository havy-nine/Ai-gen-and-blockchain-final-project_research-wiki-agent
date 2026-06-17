# Technical Analysis

## I = M × HBM × R

This project uses the framing `I = M × HBM × R`, where intelligent behavior comes from model capability, hardware/budget constraints, and retrieval/tool/state integration.

## M: Model

Current providers:

- `mock`: deterministic fallback for stable demonstrations and CI-style runs.
- `ollama`: local LLM option, default model `qwen2.5:3b`.
- `openai`: OpenAI Responses API option with `OPENAI_API_KEY` and `OPENAI_MODEL`.

Latest evidence run requested `ollama`, used `eval_provider_requested: mock` for runtime, and records `llm_provider_used: mock+ollama` with fallback disclosed. The project is designed so reviewers can run without paid credentials, while still supporting stronger providers.

## HBM: Hardware, Budget, Memory

- Mock mode has zero API cost and stable latency.
- Ollama mode keeps data local but depends on local CPU/RAM and running server.
- OpenAI mode can improve writing quality but sends source text externally and incurs token cost.
- Obsidian stores notes locally and provides graph memory.
- `usage_log/RUN_LOG.jsonl` stores structured run memory.

## R: Retrieval, Tools, MCP, Memory, External State

Retrieval/tool/state components:

- PDF extraction and chunking: `src/pipeline/chunker.py`.
- Wiki generation: `src/agents/curator.py`.
- Verification: `src/agents/evaluator.py`.
- Reward logging: `src/agents/payer.py`.
- Mock certificate registry: `src/blockchain/mock_chain.py`.
- Daily memory: `usage_log/` and `obsidian_vault/Daily Logs/`.
- Graph state: `obsidian_vault/Research Topics/` and paper links.

## Why This Is an Agent, Not Just a Chatbot

The system executes a workflow with tools and state:

1. reads files,
2. extracts/chunks documents,
3. generates structured notes,
4. evaluates claims against source evidence,
5. records logs and mock tx evidence,
6. builds a persistent Obsidian vault,
7. requires human review for risky real-world actions.

A chatbot would only answer one prompt; this system changes project-local artifacts and creates a daily research memory.

## Verification

- PASS requires `score_bps >= threshold_bps` and no critical unsupported claim.
- FAIL pages remain local-only.
- Mock certificate records are generated only for PASS pages.
- Obsidian wikilinks are validated for `missing_count 0` during manual QA.
- `basedpyright` currently reports 0 errors and 0 warnings for project configuration.

## Failures and Fixes

- System-wide Ollama install failed because `sudo` required a password; fixed by user-local install.
- Obsidian initially opened the wrong vault; fixed by registering `obsidian_vault/` and creating `demo/open_obsidian_vault.sh`.
- Early Obsidian links were broken because generated links used display titles; fixed by rewriting links to actual file stems.
- Latest large run requested Ollama, used mock evaluation for runtime, and disclosed fallback status; OpenAI runs still require an API key.
