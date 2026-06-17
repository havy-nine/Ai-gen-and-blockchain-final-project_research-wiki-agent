# Final Demo Video Guide

Target length: 4-5 minutes.

## 0:00-0:30 Problem

Show that the project is a local-first LLM research wiki for AI/robotics papers. Explain that the goal is not just summarization, but paper organization, source-backed research notes, and PASS-only mock certification.

## 0:30-1:20 Open the Obsidian Research Portal

```bash
obsidian /home/cheon/Documents/workspace/ai_blockchain/final_submission_research_wiki/vault
```

Show:

- `Research Dashboard.md`
- Method Map
- Task Map
- Dataset Map
- Graph View with clean filter already applied

## 1:20-2:10 Show Wiki Search in Terminal

```bash
python demo/wiki_search_cli.py --query "robot manipulation diffusion policy vision language action" --wiki-dir output/wiki_final_demo --mode semantic --limit 5
```

Point out that each result includes source PDF and Obsidian link.

## 2:10-3:10 Show Natural-Language Research Note

```bash
python demo/research_note_cli.py --query "로봇 조작 연구에서 vision-language-action 모델, diffusion policy, 대규모 로봇 데이터셋을 비교하고 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 출처와 함께 정리해줘" --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --provider ollama --limit 7
```

Open the generated note under `Research Notes/` and show `Related Papers With Sources`.

## 3:10-4:00 Show Drag-Drop PDF Flow

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir final_submission_research_wiki/wiki_dragdrop_demo --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Use menu `1`, drag a PDF path, then menu `3`. Then use menu `5` to type a research topic and show related papers with sources.

## 4:00-4:40 Honest Limits

Say:

- Ollama local LLM is used, with deterministic fallback recorded honestly for stability.
- Certificate/payment outputs are mock, not real WorldLand tx or real WLC payment.
- FAIL fixture remains local-only and is hidden from the clean graph.
