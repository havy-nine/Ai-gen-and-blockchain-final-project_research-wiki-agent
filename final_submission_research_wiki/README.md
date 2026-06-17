# Final Submission Research Wiki Demo

이 폴더는 최종 제출용으로 정리한 local-first LLM research wiki demo입니다. 핵심은 PDF를 넣으면 paper page로 구조화하고, 사용자의 자연어 연구 메모를 관련 paper citation과 함께 Obsidian에 저장하는 것입니다.

## What This Demo Shows

- Local LLM path: `ollama` with `qwen2.5:3b` was started locally and used in the final run.
- PDF drag-drop path: terminal에 PDF 경로를 붙여넣거나 `--add-file`로 넣으면 source folder에 저장되고 wiki page가 생성됩니다.
- Research note path: 자연어 연구 질문을 입력하면 관련 paper를 sentence-transformer similarity로 찾고, source PDF와 Obsidian page citation을 포함한 note를 만듭니다.
- Obsidian portal: 단순 paper list가 아니라 `Research Dashboard`, `Source Library`, `Methods`, `Tasks`, `Research Notes`, `Evaluation` 구조로 정리합니다.
- Blockchain gate: PASS page만 mock certificate 대상이고, hallucinated fixture는 FAIL/local-only입니다.

## Main Output

Open this vault in Obsidian:

```bash
obsidian /home/cheon/Documents/workspace/ai_blockchain/final_submission_research_wiki/vault
```

Start from:

```text
Research Dashboard.md
Home.md
Research Notes/
Sources/Source Library.md
Evaluation/Certified_PASS.md
```

## Demo Paper Set

The PDF list is reproducible from the manifest. To keep the GitHub repo lightweight, source PDFs are downloaded on demand instead of committed:

```bash
python demo/download_final_demo_papers.py --output-dir data/final_demo_papers
```

Included papers:

- Diffusion Policy
- RT-1
- RT-2
- Segment Anything
- 3D Gaussian Splatting

Manifest:

```text
data/final_demo_papers/FINAL_DEMO_PAPERS_MANIFEST.json
```

## Reproduce Full Local LLM Demo

Start Ollama if needed:

```bash
nohup ollama serve > data/logs/ollama_final_demo.log 2>&1 &
```

If you want to regenerate from PDFs, download the paper set first, then run the final paper pipeline:

```bash
python demo/download_final_demo_papers.py --output-dir data/final_demo_papers
python demo/demo_pipeline.py --sources-dir data/final_demo_papers --output-dir output/wiki_final_demo --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Build and enhance the Obsidian vault:

```bash
python demo/build_obsidian_vault.py --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --min-source-files 1
python demo/enhance_research_portal.py --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault
```

Create a natural-language research note:

```bash
python demo/research_note_cli.py --query "로봇 조작 연구에서 vision-language-action 모델과 diffusion policy를 비교하고, 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 정리해줘" --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --provider ollama --limit 5
```

## Drag-Drop PDF Demo

For actual terminal drag/drop, run. The source folder is created/populated at runtime:

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir final_submission_research_wiki/wiki_dragdrop_demo --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Then choose:

```text
1 → drag PDF path → Enter → 3 → 4
```

Non-interactive verified command:

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir final_submission_research_wiki/wiki_dragdrop_demo --add-file data/final_demo_papers/Diffusion_Policy_Visuomotor_Policy_Learning.pdf --run-pipeline --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

## Verified Results

See `FINAL_DEMO_SUMMARY.json`.

Important honesty notes:

- `mock+ollama` means Ollama was used where available and deterministic mock paths remain for stable demo components such as the fail fixture.
- No real WorldLand transaction was sent.
- No real WLC payment was sent.
- Mock certificate/payment hashes are demo evidence, not explorer transactions.

## Latest Expanded Final Demo

- Paper PDFs: `13`
- Final run: `run_20260616_114325`
- Obsidian clean graph: enabled in `vault/.obsidian/graph.json`
- Terminal search: `python demo/wiki_search_cli.py --query "robot manipulation diffusion policy" --wiki-dir output/wiki_final_demo --mode semantic --limit 5`
- Natural-language research note: `python demo/research_note_cli.py --query "..." --wiki-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --provider ollama --limit 7`
- Video guide: `VIDEO_GUIDE.md`
- Change summary: `WHAT_CHANGED.md`

## Easier Integrated CLI Flow

You can now use one menu-based CLI for PDF drag-drop, pipeline run, and research-topic note generation:

```bash
python demo/source_drop_cli.py --sources-dir final_submission_research_wiki/dragdrop_sources --output-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

Menu:

```text
1 파일 추가
2 텍스트 추가
3 pipeline 실행
4 종료
5 연구주제 입력
```

Non-interactive research-topic shortcut:

```bash
python demo/source_drop_cli.py --output-dir output/wiki_final_demo --vault-dir final_submission_research_wiki/vault --research-query "내 연구주제" --research-provider ollama --research-limit 5 --no-interactive
```
