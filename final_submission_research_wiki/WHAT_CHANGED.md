# What Changed For Final Submission

## Graph Cleanup

- Added clean Obsidian graph filter that hides `Daily Logs`, `Evidence`, `Evaluation`, `_hidden`, hallucinated fixture, and FAIL-local-only nodes.
- Enabled `hideUnresolved` and color groups for Pages, Methods/Tasks/Datasets, and Research Notes.
- Expanded the research portal hierarchy with `Methods`, `Tasks`, `Datasets`, `Sources`, `Evaluation`, `Reading Queue`, and `Research Dashboard`.

## Paper Set Expansion

Expanded the final demo paper set from 5 to 13 PDFs:

- Diffusion Policy
- RT-1
- RT-2
- PerAct
- PaLM-E
- Open X-Embodiment
- Segment Anything
- DETR
- DINOv2
- CLIP
- LLaVA
- NeRF
- 3D Gaussian Splatting

## Terminal Research Tools

- Added `demo/wiki_search_cli.py` for terminal wiki search.
- Supports semantic search with sentence-transformers and keyword search with JSON output.
- Existing `demo/research_note_cli.py` generates Obsidian research notes from natural-language queries and includes related paper source citations.

## Verified Final Run

- Run ID: `run_20260616_114325`
- Source PDFs: `13`
- Chunks: `162`
- Pages: `14`
- PASS / FAIL: `13 / 1`
- Mock certificate tx: `13`
- Mock payment tx: `43`
- LLM requested: `ollama`
- Provider used: `mock+ollama`

## Files To Open

- Final folder: `final_submission_research_wiki/`
- Final vault: `final_submission_research_wiki/vault/`
- Demo summary: `final_submission_research_wiki/FINAL_DEMO_SUMMARY.json`
- Video guide: `final_submission_research_wiki/VIDEO_GUIDE.md`
