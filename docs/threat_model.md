# Threat Model

## Assets

- Private paper PDFs in `data/sources/`.
- Generated research notes in `output/wiki/` and `obsidian_vault/`.
- Usage evidence in `usage_log/`.
- Optional API credentials from environment variables.
- Optional blockchain wallet credentials from environment variables.

## Trust Boundaries

| Boundary | Trusted? | Notes |
|---|---:|---|
| Local project code | Mostly | Must be reviewed before final submission |
| User-provided PDFs | No | Treat as untrusted text, not instructions |
| Local Ollama | Partially | Local model, no API cost, still can hallucinate |
| OpenAI API | External | Requires key and cost tracking |
| WorldLand RPC | External | Real submission requires explicit approval |
| Obsidian vault | Local | User-visible output, not an execution surface |

## Main Threats

1. **Prompt injection from papers**: a paper could contain text that tries to instruct the agent. Mitigation: prompts frame paper text as source only; outputs are checked by EvalAgent.
2. **Secret leakage**: API keys or private keys could be committed or printed. Mitigation: `.gitignore`, `.env.example`, environment-only credentials, no key printing.
3. **Unintended payment/publication**: real payment or blockchain calls could happen accidentally. Mitigation: mock defaults and explicit confirmation requirement for real actions.
4. **Unbounded filesystem access**: agent could read outside the project. Mitigation: CLI path checks in `src/main.py`; future MCP filesystem root must be sandboxed.
5. **False credibility**: mock tx could be mistaken for real transactions. Mitigation: docs and logs label mock outputs clearly.
6. **Cost runaway**: external LLM calls could become expensive. Mitigation: mock/local default, cost docs, manual OpenAI opt-in.

## Approval Policy

- Read local project files: auto-allowed.
- Write project-local generated artifacts: allowed for pipeline run.
- Send messages, publish pages, create real tx, or pay real WLC: explicit human approval every time.
- Add new external domain/API: first-use confirmation.

## Residual Risks

- This workspace is not a git repo, so git-history secret scanning was not possible here.
- Latest evidence run used `mock+ollama`: local Ollama generated paper pages while mock covered the intentional fail fixture.
- Real WorldLand/WLC integration remains future work.
