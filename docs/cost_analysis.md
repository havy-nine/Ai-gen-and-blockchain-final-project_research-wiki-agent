# Cost Analysis

## Current Evidence Run

Latest real appended representative run:

- Run ID: `run_20260604_121901`
- Provider used: `mock+ollama`
- Source PDFs: 107
- Chunks: 1306
- Pages: 108
- External LLM cost: `$0.00`
- Blockchain cost: `$0.00` because mock chain is used; exported certificate payloads do not submit transactions
- WLC payment cost: `$0.00` real cost because mock payment is used

## Model Options

| Tier | Provider | Use | Cost |
|---|---|---|---|
| Cheap/stable | `mock` | deterministic demo, CI, fallback | $0 |
| Local | `ollama` with `qwen2.5:3b` | private routine paper summarization | API cost $0, local CPU/RAM time |
| Stronger external | `openai` | better summaries or final verification | pay-per-token, requires `OPENAI_API_KEY` |

## Two-Tier Strategy

1. Use mock or local Ollama for daily routine ingestion.
2. Use OpenAI only for difficult summaries, final report polishing, or reviewer-facing verification.
3. Keep blockchain and payment in mock mode unless the user explicitly approves real transactions after MetaMask/faucet setup.

## Cost Estimate

The project does not currently measure exact token counts. A conservative planning estimate:

- One paper page prompt may include up to about 9,000 source characters.
- Seven papers plus evaluation prompts can create dozens of LLM calls.
- Mock mode remains free and safe for repeated daily evidence.
- Ollama mode has no API cost but can be slower and lower quality.
- OpenAI mode should be treated as opt-in and monitored per run.

## Monthly Cost Control

Target daily workflow:

- 1-3 papers per day.
- Default: local/mock run.
- External OpenAI: only when a better generated page is needed.
- Hard cap recommendation: warn the user before running OpenAI on more than 10 PDFs in one batch.

## Current Limitation

No exact token/cost logger is implemented yet. `docs/mcp_plan.md` proposes `estimate_cost(input_tokens, output_tokens, model)` as a custom tool for future integration.
