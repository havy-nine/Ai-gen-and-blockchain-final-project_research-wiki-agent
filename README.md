# WorldLand Knowledge Wiki Agent

## Team

- Team name: Research Wiki Agent
- Members: Cheon Seungyeon / 천승연

## Primary Project Type

Research/Study Copilot

## Problem Statement and Target User

Researchers and AI students collect papers faster than they can organize, search, verify, and connect them. The target user is a researcher who wants a private, repeatable workflow for turning paper PDFs into structured research notes, source-backed wiki pages, and auditable study logs.

WorldLand Knowledge Wiki Agent helps by running a tool-using pipeline: ingest sources, generate wiki pages, evaluate claims against evidence, record usage logs, and keep failed or hallucinated pages local-only.

## Installation and Execution

The runnable implementation is in [`./code`](code/).

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

Interactive CLI for PDF path input and research-topic input:

```bash
cd code
python demo/source_drop_cli.py --sources-dir ../tmp_sources --output-dir ../tmp_wiki --llm-provider mock --eval-provider mock --mock-chain --mock-payment
```

## Differentiation vs Big-Tech Assistants

This project is not a generic chatbot or cloud-only assistant. It focuses on a local-first research workflow with explicit logs and a blockchain-style publication gate. Generated knowledge pages are evaluated before publication; PASS pages can receive mock certificate records, while FAIL pages remain local-only and are not certified.

The key difference is auditability: the project records source processing, claim evaluation, certificate decisions, and mock payment evidence instead of only returning a conversational answer.

## 7-Day Usage Log Summary

The usage log is stored at [`./usage-log/USAGE_LOG.md`](usage-log/USAGE_LOG.md). Supporting logs are also included in [`./usage-log`](usage-log/):

- `RUN_LOG.jsonl`
- `EVALUATION_LOG.md`
- `CERTIFICATE_LOG.md`
- `PAYMENT_LOG.md`

The logs document real development/demo runs and explicitly record fallback behavior, PASS/FAIL outcomes, mock certificate records, and mock payment records.

## Cost Estimate and Local/Cloud Stack

Default submission mode uses local/mock execution and requires no paid API call. Ollama can run locally with no per-token cloud charge when installed. Optional OpenAI mode is supported through environment variables, but it is not required for the submitted demo.

Blockchain and payment actions in this repository are mock-only, so the submitted workflow has no real gas cost and sends no real WLC payment.

## Privacy/Security Summary

The default workflow is local-first. `.env` files, private keys, PEM files, and wallet files are ignored by git. The demo does not print private keys and does not claim real WorldLand transactions or real WLC payments.

Real payment or public-chain publication would require explicit human approval and is outside the default safe path.

## Demo Video

Demo video folder: [`./demo-video`](demo-video/)

Status: pending upload/link. The final video should be under 5 minutes.

## Final Deliverables

- Code: [`./code`](code/)
- Slides: [`./slides`](slides/) - placeholder folder, final slides pending
- Paper: [`./paper`](paper/) - placeholder folder, final report pending
- Usage Log: [`./usage-log`](usage-log/)
- Demo Video: [`./demo-video`](demo-video/)
