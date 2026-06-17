# WorldLand Knowledge Wiki Agent

WorldLand Knowledge Wiki Agent is a local-first LLM research wiki for AI/robotics papers with an Obsidian knowledge graph and a blockchain-style trust layer. It ingests PDFs, generates source-backed research pages, evaluates claims with a PASS/FAIL publication gate, and records mock certificate/payment evidence for accepted pages only.

## Team

- Team: Research Wiki Agent
- Member: Cheon Seungyeon / 천승연
- Course: GIST Generative AI & Blockchain 2026
- Project type: Research productivity agent + blockchain trust/audit layer

## Required Final Links

- Code: [`code/`](code/) plus implementation in [`src/`](src/), [`demo/`](demo/), [`contracts/`](contracts/)
- Paper/report: [`paper/final_paper.md`](paper/final_paper.md)
- Slides: [`slides/`](slides/) and [Google Slides](https://docs.google.com/presentation/d/1WqsB2zNNv3m6rWKDrs80DrgwbpdcoKXO/edit?usp=drive_link&ouid=102887403624877826545&rtpof=true&sd=true)
- Usage log: [`usage-log/USAGE_LOG.md`](usage-log/USAGE_LOG.md)
- Demo video: [`demo-video/README.md`](demo-video/README.md) - add uploaded video URL after recording
- Final demo package: [`final_submission_research_wiki/`](final_submission_research_wiki/)
- Final demo summary: [`final_submission_research_wiki/FINAL_DEMO_SUMMARY.json`](final_submission_research_wiki/FINAL_DEMO_SUMMARY.json)
- Final paper manifest: [`data/final_demo_papers/FINAL_DEMO_PAPERS_MANIFEST.json`](data/final_demo_papers/FINAL_DEMO_PAPERS_MANIFEST.json)

## Problem and Target User

Researchers collect papers faster than they can organize, cite, verify, and connect them. This project targets AI researchers who want a private research vault that turns paper PDFs into linked notes, source-backed research memos, and auditable publication decisions.

## What Works Now

- PDF path paste / drag-drop through `demo/source_drop_cli.py`.
- Natural-language research-topic input that returns related papers with source citations.
- Obsidian vault output with dashboard, source library, methods, tasks, datasets, pages, graph view, and research notes.
- PASS-only mock certificate registry: passed pages receive mock certificate records; failed pages stay local-only with `SKIP_CHAIN`.
- Mock payment log for accepted EvalAgent findings.

## Quick Demo Commands

Open the final Obsidian vault:

```bash
obsidian /home/cheon/Documents/workspace/ai_blockchain/final_submission_research_wiki/vault
```

Run the integrated CLI for PDF input, pipeline execution, and research-topic search. The `dragdrop_sources` folder is created at runtime when a PDF path is pasted or passed with `--add-file`:

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Run semantic wiki search:

```bash
python demo/wiki_search_cli.py --query "robot manipulation diffusion policy vision language action" --wiki-dir output/wiki_final_demo --mode semantic --limit 5
```

Create a source-backed research note:

```bash
python demo/research_note_cli.py --query "로봇 조작 연구에서 vision-language-action 모델, diffusion policy, 대규모 로봇 데이터셋을 비교하고 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 출처와 함께 정리해줘" --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --provider ollama --limit 7
```

## Final Demo Evidence

To keep the repository lightweight, source PDFs are not committed. Recreate them from the manifest when needed:

```bash
python demo/download_final_demo_papers.py --output-dir data/final_demo_papers
```

The generated wiki and Obsidian vault are committed for review. Representative final run: `run_20260616_114325`

- Source PDFs: 13
- Chunks: 162
- Pages: 14
- PASS / FAIL: 13 / 1
- Threshold: 7800 bps
- Mock certificates: 13
- Mock payments: 43
- Requested provider: Ollama
- Recorded provider: `mock+ollama` with deterministic fallback disclosure when timed out

See [`final_submission_research_wiki/FINAL_DEMO_SUMMARY.json`](final_submission_research_wiki/FINAL_DEMO_SUMMARY.json).

## Cost, Privacy, and Security

The default demo is local/mock-first. Ollama is used when available, with deterministic fallback recorded in logs. OpenAI support is optional and requires an API key. The demo does not claim real WorldLand transactions or real WLC payments. Real payment/publication actions require explicit human approval and are outside the default safe path. Private keys are not printed, and `.env` files are ignored.

## Differentiation

This is not a generic chatbot. It is a tool-using research workflow that reads PDFs, builds a persistent Obsidian graph, evaluates generated claims against sources, records audit logs, and separates local drafts from publication-certified pages.

## Repository Structure

```text
code/                         Required code pointer directory
src/                          Core pipeline and agents
demo/                         CLI demos and vault builders
contracts/                    Certificate registry smart contract
paper/                        Final report files
slides/                       Final presentation files and link
usage-log/                    Required usage log folder
demo-video/                   Demo video link placeholder
final_submission_research_wiki/ Final Obsidian/demo artifact
output/wiki_final_demo/       Generated wiki pages for final demo
data/final_demo_papers/       Final 13-paper manifest; PDFs are downloaded on demand
```

## Honest Limitations

- No real WorldLand tx hash is claimed.
- No real WLC payment is claimed.
- Certificate/payment outputs in the demo are mock records.
- The demo video URL must be added after recording.
