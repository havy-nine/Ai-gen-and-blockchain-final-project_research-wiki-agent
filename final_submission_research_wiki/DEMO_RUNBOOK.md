# Demo Runbook

## 1. Open the final vault

```bash
obsidian /home/cheon/Documents/workspace/ai_blockchain/final_submission_research_wiki/vault
```

Show `Research Dashboard.md`, then open `Research Notes/` and one linked paper page.

## 2. Show PDF drag-drop flow

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir final_submission_research_wiki/wiki_dragdrop_demo --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Use menu `1`, drag a PDF, then menu `3`.

## 3. Show natural language research note flow

```bash
python demo/research_note_cli.py --query "로봇 조작 연구에서 vision-language-action 모델과 diffusion policy를 비교하고, 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 정리해줘" --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --provider ollama --limit 5
```

Open the generated note and point to `Related Papers With Sources`.
