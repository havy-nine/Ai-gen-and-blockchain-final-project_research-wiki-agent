# Demo Video Recording Commands

Target length: under 5 minutes.

Run all commands from the repository root unless a command explicitly changes into `code/`.

## 1. Prepare Terminal

```bash
cd /home/cheon/Documents/workspace/ai_blockchain
cd code
```

Optional clean demo folders:

```bash
rm -rf data/final_demo_papers output/wiki_demo_recording ../tmp_sources ../tmp_wiki
mkdir -p data/final_demo_papers output/wiki_demo_recording
```

## 2. Start Ollama

Check Ollama:

```bash
ollama --version
```

Start the local Ollama server in the background:

```bash
nohup ollama serve > ../ollama_demo.log 2>&1 &
```

Wait 3-5 seconds, then pull the demo model:

```bash
ollama pull qwen2.5:3b
```

Optional health check:

```bash
ollama list
```

## 3. Download a Small Paper Set

For a short video, use 3 papers. This keeps the run faster while still showing the full workflow:

```bash
python demo/download_final_demo_papers.py --dest-dir data/final_demo_papers --limit 3
```

If you want the full paper set instead:

```bash
python demo/download_final_demo_papers.py --dest-dir data/final_demo_papers
```

## 4. Run the Pipeline With Ollama

```bash
python demo/demo_pipeline.py \
  --sources-dir data/final_demo_papers \
  --output-dir output/wiki_demo_recording \
  --threshold-bps 7800 \
  --llm-provider ollama \
  --eval-provider ollama \
  --mock-chain \
  --mock-payment \
  --append-usage-log
```

What to say in the video:

- The system reads PDFs, chunks text, creates wiki pages, evaluates claims, and records logs.
- PASS pages get mock certificate records.
- FAIL pages stay local-only with `SKIP_CHAIN`.
- The demo does not claim real WorldLand transactions or real WLC payments.

## 5. Show Generated Wiki Files

```bash
ls output/wiki_demo_recording
```

Open one generated Markdown page:

```bash
sed -n '1,120p' output/wiki_demo_recording/*.md
```

If `sed` output is too long for recording, open the folder in your file manager or editor instead.

## 6. Show Usage and Evaluation Logs

From the repository root:

```bash
cd ..
sed -n '1,80p' usage-log/USAGE_LOG.md
sed -n '1,80p' usage-log/EVALUATION_LOG.md
```

## 7. Interactive PDF/Text CLI Demo

Go back to `code/`:

```bash
cd code
```

Start the menu CLI:

```bash
python demo/source_drop_cli.py \
  --sources-dir ../tmp_sources \
  --output-dir ../tmp_wiki \
  --llm-provider ollama \
  --eval-provider ollama \
  --mock-chain \
  --mock-payment
```

Menu flow to show:

```text
1 = add PDF/TXT/MD path
2 = add typed text
3 = run pipeline
4 = exit
5 = enter research topic
```

Fast path for video if you do not want to type a PDF path manually:

```bash
python demo/source_drop_cli.py \
  --sources-dir ../tmp_sources \
  --output-dir ../tmp_wiki \
  --add-file data/final_demo_papers/Diffusion_Policy_Visuomotor_Policy_Learning.pdf \
  --run-pipeline \
  --threshold-bps 7800 \
  --llm-provider ollama \
  --eval-provider ollama \
  --mock-chain \
  --mock-payment \
  --no-interactive
```

## 8. Research Topic Query Demo

After generating `output/wiki_demo_recording`, run:

```bash
python demo/research_note_cli.py \
  --query "robot manipulation with vision-language-action models and diffusion policy" \
  --wiki-dir output/wiki_demo_recording \
  --vault-dir ../tmp_vault \
  --provider ollama \
  --limit 5
```

Then show the generated note:

```bash
find ../tmp_vault -type f | sort
```

## 9. Obsidian Option

If Obsidian is installed, build a vault from the generated wiki:

```bash
python demo/build_obsidian_vault.py \
  --wiki-dir output/wiki_demo_recording \
  --vault-dir ../tmp_obsidian_vault \
  --min-source-files 1
```

Open it:

```bash
obsidian /home/cheon/Documents/workspace/ai_blockchain/tmp_obsidian_vault
```

Show:

- `Home.md`
- generated paper pages
- graph view
- source-backed links

## 10. Final 20-Second Closing Script

Say:

```text
This is a local-first research/study copilot. It organizes papers into wiki pages, evaluates claims against source text, and records PASS/FAIL evidence. Blockchain and payment outputs are mock-only in this submission: no real WorldLand transaction or real WLC payment is claimed.
```
