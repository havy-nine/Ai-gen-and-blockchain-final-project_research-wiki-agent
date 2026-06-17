# Final Presentation Outline

Target length: 10-12 minutes.

## 1. Problem and Target User (1 min)

- AI students read many papers but lose track of summaries, claims, links, and daily progress.
- Target user: a researcher maintaining a private Obsidian vault.

## 2. Project Identity (1 min)

- Research Productivity Agent with Blockchain Agent trust layer.
- Not a chatbot: it reads files, writes notes, evaluates claims, logs runs, and builds a persistent vault.

## 3. Architecture (2 min)

Show `docs/workflow.md` or `PRESENTATION_DEMO.html`.

```text
PDF -> chunker -> CuratorAgent -> EvalAgent -> mock certificate/payment logs -> Obsidian vault -> human review
```

## 4. Live Demo (3 min)

Commands:

```bash
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider ollama --eval-provider mock --mock-chain --mock-payment --append-usage-log
python demo/build_obsidian_vault.py
./demo/open_obsidian_vault.sh
```

Show:

- `Home.md`
- `Research Topics/AI Research Atlas.md`
- Graph View
- `Daily Logs/Daily_Research_Log_2026_06_04.md`

## 5. Trust, Security, Cost (2 min)

- PASS/FAIL gate in basis points.
- Failed page remains local-only.
- Mock tx hashes are clearly labeled.
- No real WorldLand/WLC claims.
- Cost modes: mock/local/OpenAI.

## 6. Evidence (1 min)

Show:

- `usage_log/USAGE_LOG.md`
- `usage_log/RUN_LOG.jsonl`
- `evidence/threshold_curve.png`
- `evidence/reward_comparison.png`

## 7. Limitations and Next Steps (1 min)

- Latest run requested local Ollama for generated paper pages, used mock evaluation for runtime, and disclosed fallback behavior.
- Need seven consecutive daily entries if strictly required.
- Real blockchain/payment integration remains future work with explicit approval.
- GitHub repository setup still needed in this workspace.
