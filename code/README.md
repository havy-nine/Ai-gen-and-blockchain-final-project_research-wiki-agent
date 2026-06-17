# Code

This folder contains the runnable implementation for the final project.

## Main Components

- `src/`: core pipeline, agents, LLM client, hashing, and mock blockchain tools
- `demo/`: CLI demos, pipeline runner, vault builder, paper downloader, and research note tools
- `contracts/`: certificate registry smart contract
- `mcp_servers/`: optional MCP-style research vault server
- `tests/`: lightweight package/test scaffold

## Quick Run

```bash
python -m pip install -r requirements.txt
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider mock --eval-provider mock --mock-chain --mock-payment --append-usage-log
```

Run the PDF/research-topic CLI:

```bash
python demo/source_drop_cli.py --sources-dir ../tmp_sources --output-dir ../tmp_wiki --llm-provider mock --eval-provider mock --mock-chain --mock-payment
```
