# WorldLand Knowledge Wiki Agent

WorldLand Knowledge Wiki Agent is a research productivity agent with a blockchain-style trust layer. It converts paper PDFs into source-backed wiki pages, evaluates generated claims with a PASS/FAIL gate, and records mock certificate/payment evidence for auditability.

## Team

- Team: Research Wiki Agent
- Member: Cheon Seungyeon / 천승연
- Course: GIST Generative AI & Blockchain 2026
- Project type: Research productivity agent + blockchain trust/audit layer

## Required Final Links

- Code: [`code/`](code/)
- Slides: [`slides/`](slides/) - placeholder folder, final file/link pending
- Paper/report: [`paper/`](paper/) - placeholder folder, final file pending
- 7-day usage log: [`usage-log/USAGE_LOG.md`](usage-log/USAGE_LOG.md)
- Demo video: [`demo-video/README.md`](demo-video/README.md) - upload link pending

## Target User and Usefulness

Target users are AI researchers or students who collect many papers and need a repeatable way to organize, search, and verify research notes. The system is useful because it turns paper ingestion into a tool-using workflow: read sources, generate wiki pages, evaluate claims, record logs, and keep failed/hallucinated pages local-only.

## Differentiation From Big-Tech AI Tools

This project is not a generic chatbot or cloud-only notebook. It focuses on a private, reproducible local workflow with explicit evidence logs and a publication gate. The blockchain component is used as a certificate registry concept: only pages that pass the EvalAgent threshold are eligible for mock certification; failed pages are not published.

## Execution Steps

From the repository root:

```bash
cd code
python -m pip install -r requirements.txt
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider mock --eval-provider mock --mock-chain --mock-payment --append-usage-log
```

Optional local LLM mode, if Ollama is installed:

```bash
cd code
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

The interactive CLI for PDF path input and research-topic input is:

```bash
cd code
python demo/source_drop_cli.py --sources-dir ../tmp_sources --output-dir ../tmp_wiki --llm-provider mock --eval-provider mock --mock-chain --mock-payment
```

## Cost Estimate

Default demo mode uses local/mock execution and has no required API cost. Ollama local inference can run on the user's machine with no per-token cloud charge. Optional OpenAI mode is supported by environment variable but is not required for submission. Blockchain/payment actions in this repo are mock-only, so there is no real gas cost or WLC transfer in the submitted demo.

## Privacy and Security Summary

The default workflow is local-first. `.env` files, private keys, PEM files, and wallet files are ignored by git. The demo does not print private keys and does not claim real WorldLand transactions or real WLC payments. Real payment or public-chain publication would require explicit human approval and is outside the default safe path.

## Submission Status

- GitHub repository: public repo expected at `https://github.com/havy-nine/Ai-gen-and-blockchain-final-project_research-wiki-agent`
- Code folder: present
- Slides folder: present, intentionally empty for now
- Paper folder: present, intentionally empty for now
- Usage log: present
- Demo video: pending upload/link
- Course repo PR: pending
