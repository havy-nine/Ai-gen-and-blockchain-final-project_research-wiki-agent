# Differentiation

## 1. Privacy by Default

Evidence:

- Default safe run uses local files and mock provider; the latest large run requested local Ollama and mock evaluation.
- Source PDFs remain under `data/sources/`.
- Obsidian output is local in `obsidian_vault/`.
- Ollama can run locally when selected.

Why it matters: AI paper notes and research direction can remain private instead of being sent to a hosted chatbot by default.

## 2. Cost Transparency

Evidence:

- `docs/cost_analysis.md` states which modes cost money.
- Latest run requested `ollama`, used mock evaluation and mock chain/payment, and records fallback status, so no paid API or real-chain cost was incurred.
- Logs record provider used and fallback status.

Why it matters: the user can demonstrate daily use without uncontrolled API spending.

## 3. Customization

Evidence:

- The workflow is specific to AI paper intake across major fields.
- The generated vault includes a custom topic page: `AI Research Atlas`.
- EvalAgent uses basis-point thresholds and critical unsupported-claim gates.

Why it matters: this is not a generic chatbot; it is tuned to a research note workflow.

## 4. Composability

Evidence:

- Combines filesystem ingestion, PDF extraction, LLM provider abstraction, evaluation, mock blockchain certificate, mock payment reward, logs, and Obsidian vault generation.
- MCP plan documents future filesystem/fetch/memory/sqlite/github tool servers.

Why it matters: each tool has a bounded role and can be replaced or extended.

## 5. Self-Improvement Path

Evidence:

- Daily logs accumulate in `usage_log/RUN_LOG.jsonl` and `obsidian_vault/Daily Logs/`.
- Failures are recorded honestly, including mock fallback and local-only failed pages.
- Future prompts/rules can be adjusted based on failed claim patterns.

Why it matters: the agent can improve from daily usage evidence rather than one-off prompting.
