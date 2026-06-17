# USAGE_LOG.md

This log records real daily project usage for the WorldLand Knowledge Wiki Agent. Entries include timestamp, user identity, channel, task type, MCP/server component, action, outcome, and latency. Failures and fallback behavior are recorded honestly as engineering evidence.

| Date | Timestamp | User identity | Channel | Task type | MCP/server component | Action | Outcome | Latency |
|---|---|---|---|---|---|---|---|---|
| 2026-06-02 | 2026-06-02T17:48:39+09:00 | 천승연 | local CLI + Sisyphus coding agent | MVP implementation / evaluation | local-ollama, wiki-curator, eval-agent, mock-worldland-registry, pay-agent | Installed local Ollama, pulled `qwen2.5:3b`, connected CuratorAgent and EvalAgent to local LLM, ran full publication-gating pipeline. | 6 pages generated, 6 passed threshold, 0 remained local-log-only at threshold 0.7, 6 mock PageCertified events, 0.06 WLC mock rewards. | Representative pipeline 33.5s; Ollama test 392ms; Eval sample 1742ms |

## Notes

- 2026-06-02 includes a real engineering failure/recovery: system-wide Ollama installation failed because `sudo` required a password. The implementation recovered by installing Ollama under the user directory (`~/.local`) and running the server through tmux.
- The WorldLand page scored below threshold and did not create an on-chain transaction. This is desirable evidence for the publication gate.
- Future entries should be added daily, not batch-created before submission.

## run_20260602_095252
- timestamp: 2026-06-02T09:52:54.301811+00:00
- source_files: 7
- chunks: 73
- pages: 7
- threshold_bps: 7800
- pass: 6
- fail: 1
- llm_provider_used: mock

## run_20260602_095346
- timestamp: 2026-06-02T09:53:48.430793+00:00
- source_files: 7
- chunks: 73
- pages: 7
- threshold_bps: 7800
- pass: 6
- fail: 1
- llm_provider_used: mock

## run_20260602_095405
- timestamp: 2026-06-02T09:54:07.231393+00:00
- source_files: 6
- chunks: 72
- pages: 7
- threshold_bps: 7800
- pass: 6
- fail: 1
- llm_provider_used: mock

## run_20260603_050809
- timestamp: 2026-06-03T05:08:11.295357+00:00
- source_files: 6
- chunks: 72
- pages: 7
- threshold_bps: 7800
- pass: 6
- fail: 1
- llm_provider_used: mock

## run_20260604_095351
- timestamp: 2026-06-04T09:53:53.788898+00:00
- source_files: 7
- chunks: 85
- pages: 8
- threshold_bps: 7800
- pass: 7
- fail: 1
- llm_provider_used: mock

## run_20260604_113632
- timestamp: 2026-06-04T11:38:16.362940+00:00
- source_files: 7
- chunks: 85
- pages: 8
- threshold_bps: 7800
- pass: 7
- fail: 1
- llm_provider_used: mock+ollama

## run_20260604_113928
- timestamp: 2026-06-04T11:40:47.717444+00:00
- source_files: 7
- chunks: 85
- pages: 8
- threshold_bps: 7800
- pass: 6
- fail: 2
- llm_provider_used: mock+ollama

## Entry Template

Use this template for future real daily usage entries. Do not fill future dates before they happen.

```md
## YYYY-MM-DD

- Timestamp:
- User:
- Channel: CLI / Web / Telegram / Slack / Local app / Other
- Task:
- Tool or MCP server used:
- Input summary:
- Output summary:
- Latency:
- Cost estimate:
- Result:
- Failure / fix:
```

## run_20260604_121901
- timestamp: 2026-06-04T12:32:17.501074+00:00
- source_files: 107
- chunks: 1306
- pages: 108
- threshold_bps: 7800
- pass: 106
- fail: 2
- llm_provider_used: mock+ollama
- note: LLM unavailable; deterministic mock fallback used. (timed out)

## run_20260606_062955
- timestamp: 2026-06-06T06:29:56.168279+00:00
- source_files: 2
- chunks: 22
- pages: 3
- threshold_bps: 7800
- pass: 2
- fail: 1
- llm_provider_used: mock

## run_20260607_104835
- timestamp: 2026-06-07T10:49:07.438907+00:00
- source_files: 109
- chunks: 1328
- pages: 110
- threshold_bps: 7800
- pass: 109
- fail: 1
- llm_provider_used: mock

## run_20260607_182034
- timestamp: 2026-06-07T18:22:59.884756+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama
- note: LLM unavailable; deterministic mock fallback used. ('utf-8' codec can't encode character '\ud835' in position 2624: surrogates not allowed)

## run_20260607_192620
- timestamp: 2026-06-07T19:27:10.773686+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama

## run_20260607_192955
- timestamp: 2026-06-07T19:30:47.250218+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama

## run_20260607_212149
- timestamp: 2026-06-07T21:24:08.178123+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama
- note: LLM unavailable; deterministic mock fallback used. (timed out)

## run_20260607_213513
- timestamp: 2026-06-07T21:36:07.059934+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama

## run_20260607_215006
- timestamp: 2026-06-07T21:50:57.378892+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama

## run_20260607_215405
- timestamp: 2026-06-07T21:54:56.382766+00:00
- source_files: 10
- chunks: 118
- pages: 11
- threshold_bps: 7800
- pass: 10
- fail: 1
- llm_provider_used: mock+ollama

## run_20260616_074724
- timestamp: 2026-06-16T07:47:37.788986+00:00
- source_files: 5
- chunks: 62
- pages: 6
- threshold_bps: 7800
- pass: 5
- fail: 1
- llm_provider_used: mock
- note: LLM unavailable; deterministic mock fallback used.

## run_20260616_074835
- timestamp: 2026-06-16T07:49:13.605091+00:00
- source_files: 5
- chunks: 62
- pages: 6
- threshold_bps: 7800
- pass: 5
- fail: 1
- llm_provider_used: mock+ollama

## run_20260616_075004
- timestamp: 2026-06-16T07:50:21.544000+00:00
- source_files: 1
- chunks: 13
- pages: 2
- threshold_bps: 7800
- pass: 1
- fail: 1
- llm_provider_used: mock+ollama

## run_20260616_114325
- timestamp: 2026-06-16T11:46:05.312007+00:00
- source_files: 13
- chunks: 162
- pages: 14
- threshold_bps: 7800
- pass: 13
- fail: 1
- llm_provider_used: mock+ollama
- note: LLM unavailable; deterministic mock fallback used. (timed out)
