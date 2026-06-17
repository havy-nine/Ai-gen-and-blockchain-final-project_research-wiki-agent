# Final Paper Draft

## Abstract

WorldLand Knowledge Wiki Agent is a private research productivity agent for AI papers across major fields. It converts PDF papers into an Obsidian vault, evaluates whether generated claims are grounded in source text, records daily usage evidence, and attaches a blockchain-style trust layer through mock certificate and reward logs. The project emphasizes practical daily use, privacy, cost control, and human approval for risky actions.

## Problem

Researchers often collect papers faster than they can organize them. Manual note-taking, graph linking, citation checking, and daily progress logging are repetitive but important tasks.

## System

The system follows a Goal -> Input -> Tools -> Check -> Record -> Human Review -> Output loop. The user adds PDFs, runs a CLI agent, receives Obsidian notes, reviews evaluation logs, and can show Graph View plus usage evidence.

## Implementation

Core modules are in `src/`. The pipeline reads files from `data/sources/`, generates pages in `output/wiki/`, records logs in `usage_log/`, and builds `obsidian_vault/`. The Solidity contract is certificate-only and the current safe demo uses mock chain/payment.

## Evaluation

Latest real appended run `run_20260604_121901` processed 107 PDFs into 1306 chunks and 108 pages. 106 pages passed and two pages failed local-only. The run produced 106 mock certificate records and 368 mock payment records.

## Security and Cost

Mock/local execution is the default safe path. OpenAI use is opt-in through environment variables. Real blockchain or payment actions require explicit human approval and are not performed by the default demo.

## Limitations

The latest evidence run requested local Ollama for generated paper pages and intentionally used `--eval-provider mock` for the 107-PDF run. The run log honestly records `llm_provider_used=mock+ollama` and a fallback timeout message. Real WorldLand/WLC integration is future work. The workspace is not currently a git repository, so final submission should be copied into or initialized as a GitHub repository.

## Conclusion

The project is a useful private AI research workflow rather than a one-off chatbot. It combines document ingestion, tool execution, verification, logs, and an Obsidian memory layer with a blockchain-inspired trust mechanism.
