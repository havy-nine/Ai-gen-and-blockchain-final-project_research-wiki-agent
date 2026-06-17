# MCP Summary from Lecture Slides

## 0. 확인한 자료와 근거 범위

이 요약은 workspace에서 확인 가능한 자료를 기준으로 작성했다.

| 자료 | 경로 | 이 문서에서의 사용 방식 |
|---|---|---|
| 프로젝트 발표 PPT | `worldland_knowledge_wiki_agent_presentation.pptx` | slide 4, 12, 13의 tool / WorldLand / privacy-security 근거 |
| 영어 PPT | `worldland_knowledge_wiki_agent_presentation_english.pptx` | 한국어 PPT와 동일한 slide 4, 13 cross-check |
| 원래 proposal 문서 | `Final Project Proposal.docx` | MCP plan, custom server, threat model, USAGE_LOG 예시 근거 |
| 현재 MCP plan | `docs/mcp_plan.md`, `final_submission_package/evidence/MCP_PLAN.md` | 현재 구현/확장 계획 확인 |
| 현재 threat model | `docs/threat_model.md`, `final_submission_package/evidence/THREAT_MODEL.md` | 현재 프로젝트 위험/완화책 확인 |
| MCP server 구현 | `mcp_servers/research_vault_agent.py` | 실제 구현된 custom MCP-style server와 tool 확인 |
| usage log | `usage_log/USAGE_LOG.md`, `usage_log/TOOL_CALL_LOG.jsonl` | 실제 로그 형식과 MCP tool-call evidence 확인 |

주의: workspace 안에서 별도의 “MCP lecture PPT” 파일은 확인되지 않았다. 따라서 “PPT에 나온 내용”은 현재 프로젝트 발표 PPT에서 직접 확인되는 내용만 slide number와 함께 표시했고, 원래 proposal 또는 현재 문서에서만 확인되는 내용은 별도 근거로 구분했다. PPT에서 직접 확인되지 않는 항목은 “자료에서 직접 확인되지 않음”이라고 표시했다.

## 1. MCP가 무엇인지

### PPT에서 설명하는 MCP의 정의

자료에서 직접 확인되지 않음. 현재 프로젝트 발표 PPT는 “MCP”라는 용어 자체를 정의하지 않는다. 다만 slide 4는 Agentic Workflow 안에서 다음 tool 계층을 보여준다.

- Read-only tools: `Filesystem`, `Fetch`, `Git`, `source chunks`.
- Memory / Record: `Obsidian wiki`, `certificates`, `USAGE_LOG`.
- Action tools: `certifyPage`, `mock/real WLC payment`.

즉, PPT 기준으로는 MCP의 공식 정의보다 “AI Agent가 외부 tool / memory / action을 통해 작업한다”는 구조가 확인된다.

현재 프로젝트 문서 기준으로는 `docs/mcp_plan.md`에 “MCP server is not the model. MCP server is a tool provider. The host application controls model choice, tool discovery, credentials, workspace roots, and approval policy.”라고 정리되어 있다. 그러나 이 문장은 PPT slide에서 직접 확인되는 내용은 아니다.

### AI agent 시스템에서 MCP가 필요한 이유

PPT에서 직접 확인되는 이유는 다음과 같이 해석할 수 있다.

- Agent가 source PDF/wiki를 직접 다루므로 read-only tool과 action tool을 분리해야 한다. 근거: slide 4.
- 검증된 page만 WorldLand certificate로 보내야 하므로 tool 호출 전 publication gate가 필요하다. 근거: slide 3, 5, 6.
- PDF와 wiki 본문은 local에 두고 hash/certificate metadata만 on-chain으로 보내야 한다. 근거: slide 12, 13.
- real payment나 real blockchain publication은 위험하므로 explicit approval이 필요하다. 근거: slide 13.

MCP라는 이름으로 “왜 필요한지”를 설명한 lecture requirement는 자료에서 직접 확인되지 않음.

### 기존 방식과 MCP의 차이

자료에서 직접 확인되지 않음. 다만 프로젝트 발표 PPT에서는 기존 방식과 개선 방식을 다음처럼 비교한다.

| 비교 항목 | 기존 방식 | 개선 방식 | 근거 |
|---|---|---|---|
| Blockchain 사용 | Passive Hash Logger: page 생성 후 `page_hash`, timestamp, agent name 기록 | Publication Certificate Registry: EvalAgent 검증 통과 시에만 certificate 생성 | slide 3 |
| 실패 처리 | local log와 차별성이 약함 | FAIL은 `SKIP_CHAIN`, `tx_hash=None` | slide 3, 5, 9 |
| On-chain 의미 | 단순 hash 기록 | “이 page hash는 source-grounded verification을 통과했다”는 certificate | slide 2, 5 |

## 2. PPT에 나온 MCP 구성 요소

PPT가 이 항목들을 “MCP components”라고 부르지는 않는다. 아래 표는 slide 4의 Agentic Workflow와 slide 12-13의 WorldLand/security 내용을 MCP 관점으로 재정리한 것이다.

| 구성 요소 | 역할 | AI Agent와의 관계 | Read 권한 | Write 권한 | 비고 |
|---|---|---|---|---|---|
| Read-only tools | project/source data를 읽어 agent 작업에 제공 | Agent가 입력과 근거를 얻는 tool layer | `Filesystem`, `Fetch`, `Git`, `source chunks` read | PPT 기준 없음 | slide 4. 이름 그대로 read-only로 표시됨 |
| Memory / Record | 생성 결과와 실행 증거 저장 | Agent output과 audit trail 저장소 | Obsidian wiki, certificates, USAGE_LOG read 가능 | Obsidian wiki, certificates, USAGE_LOG 기록 가능으로 해석됨 | slide 4. 구체적 권한 정책은 PPT에 없음 |
| Action tools | 외부 상태 변경 또는 transaction 준비/실행 | Agent가 gate 이후 호출하는 위험도가 높은 tool | payment/certificate 상태 조회 여부는 PPT에서 직접 확인되지 않음 | `certifyPage`, mock/real WLC payment | slide 4, 12. real action은 approval 필요 slide 13 |
| Check / EvalAgent gate | claim groundedness 평가, PASS/FAIL 결정 | Action tool 호출 전 verifier | source chunks와 page claims read | 평가 log write는 slide 9에서 간접 확인 | slide 5-6, 9 |
| Human Review | risky action 전 사람이 확인 | Agent action의 approval boundary | review 대상 read | 승인 여부 기록 여부는 PPT에서 직접 확인되지 않음 | slide 4, 13 |
| WorldLand / certificate registry | 검증 통과 page의 hash/cert metadata 기록 | Agent output의 blockchain trust layer | latest state/tx read는 slide에서 직접 확인되지 않음 | page hash, cert hash, score/threshold metadata write | slide 12-13 |
| Secret handling | private key/API key 보호 | Agent와 MCP server가 직접 노출하면 안 되는 credential boundary | env var에서 key read 가능 | `.env` commit 금지, key 출력 금지 | slide 13 |

## 3. PPT에 나온 MCP 서버/도구 목록

### PPT slide에서 직접 확인되는 server/tool

| 이름 | 하는 일 | 어떤 데이터를 읽는지 | 어떤 데이터를 쓰는지 | final project에서 어떻게 사용할 수 있는지 | slide number 또는 근거 위치 |
|---|---|---|---|---|---|
| Filesystem | local file 접근 | source files, wiki files로 해석 가능 | PPT 기준 직접 확인되지 않음 | local Markdown/PDF/wiki 자료를 agent가 읽는 read-only tool | slide 4 |
| Fetch | 외부 URL/content 가져오기 | public web content로 해석 가능 | PPT 기준 없음 | user-provided URL이나 paper metadata import | slide 4 |
| Git | version/history 접근 | git history 또는 project snapshot | PPT 기준 없음 | generated wiki/log 변경 이력 확인 | slide 4 |
| source chunks | PDF/text chunk 근거 제공 | source chunk text | 없음 | EvalAgent가 claim groundedness를 검증할 때 사용 | slide 4, 6 |
| Obsidian wiki | 생성된 Markdown wiki 저장소 | wiki page | wiki page | final output인 Obsidian vault 구성 | slide 4 |
| certificates | 검증 통과 page certificate 저장 | certificate metadata | certificate JSON / registry record | PASS page의 certificate evidence | slide 4, 5, 12 |
| USAGE_LOG | project usage evidence 기록 | previous usage entries | usage log entries | daily usage, run evidence, tool usage 기록 | slide 4 |
| certifyPage | page certificate payload/transaction | page hash, cert hash, score metadata로 해석 가능 | mock/real transaction or certificate registry | PASS page만 WorldLand certificate로 기록 | slide 4, 5, 12 |
| mock/real WLC payment | accepted EvalAgent finding reward flow | accepted finding/payment 대상 | mock/real WLC payment record | reward-flow demo. 실제 payment는 approval 필요 | slide 4, 11, 13 |
| WorldLand / WLC integration | certificate registry 및 payment chain | page/cert metadata, tx state로 해석 가능 | page hash, cert hash, score_bps, threshold_bps, timestamp, model/eval version, agent id | mock mode로 demo, real tx는 future work | slide 12 |

### Proposal 문서에서 확인되는 MCP-compatible tools

| 이름 | 하는 일 | 어떤 데이터를 읽는지 | 어떤 데이터를 쓰는지 | final project에서 어떻게 사용할 수 있는지 | slide number 또는 근거 위치 |
|---|---|---|---|---|---|
| Filesystem MCP Server | raw file read, Markdown page write | local raw files, Obsidian vault | Markdown wiki pages | raw folder -> Obsidian wiki 생성 | `Final Project Proposal.docx`, MCP Plan paragraph |
| Fetch MCP Server | user-provided web URL에서 text import | user-provided web URL | 직접 write 여부는 proposal에서 명확하지 않음 | paid search API 없이 web source import | `Final Project Proposal.docx`, MCP Plan paragraph |
| Git MCP Server | generated wiki/log 변경 추적 | generated wiki pages/logs/git state | version-control metadata 또는 commits 여부는 직접 확인되지 않음 | generated artifact의 version control evidence | `Final Project Proposal.docx`, MCP Plan paragraph |
| Custom `WikiKnowledgeServer` | project-specific wiki tools 제공 | wiki page, vault path, page hash 대상 | wiki page, cross-link, page hash log | MVP custom MCP server | `Final Project Proposal.docx`, MCP Plan paragraph |

### 현재 구현에서 확인되는 custom MCP-style server/tool

| 이름 | 하는 일 | 어떤 데이터를 읽는지 | 어떤 데이터를 쓰는지 | final project에서 어떻게 사용할 수 있는지 | slide number 또는 근거 위치 |
|---|---|---|---|---|---|
| `research_vault_agent` | stdio JSON-RPC custom MCP-style server | project root 내부 자료 | tool별로 다름 | 현재 제출용 custom local MCP-style demo | `mcp_servers/research_vault_agent.py`, `docs/final_submission_checklist.md` |
| `search_project_memory` | generated notes, daily logs, run summaries 검색 | `obsidian_vault`, `usage_log`, `evidence`의 Markdown | 없음 | vault/search memory MCP demo | `mcp_servers/research_vault_agent.py` lines 13-15, 30-44 |
| `export_certificate_payloads` | `certifyPage` payload export | latest run summary | `evidence/certificate_payloads_latest.json` | real tx 없이 certificate payload evidence 생성 | `mcp_servers/research_vault_agent.py` lines 18-20, 45-55 |
| `blockchain_read` | EVM/WorldLand RPC read helper | network config, latest block, balance, tx | 없음 | private key 없이 WorldLand read demo | `mcp_servers/research_vault_agent.py` lines 23-25, 56-66 |

## 4. Custom MCP Server 요구사항

| 질문 | 확인 내용 | 근거 |
|---|---|---|
| custom server 이름이 필요한지 | Proposal에는 custom MCP server 이름으로 `WikiKnowledgeServer`가 필요하다고 작성되어 있음. 현재 구현 이름은 `research_vault_agent`로 변경됨 | `Final Project Proposal.docx`; `mcp_servers/research_vault_agent.py` serverInfo |
| tool signature 몇 개가 필요한지 | Proposal에는 3개 tool signature가 명시됨: `create_wiki_page(title, content, vault_path)`, `generate_cross_links(page_path, vault_path)`, `log_page_hash(page_path, agent_id)` | `Final Project Proposal.docx` |
| input schema가 필요한지 | Proposal에 input schema가 포함됨: `title: string`, `content: string`, `page_path: string`, `vault_path: string`, `agent_id: string` | `Final Project Proposal.docx` |
| prototype bonus가 있는지 | 자료에서 직접 확인되지 않음 | 검색한 PPT/문서에서 해당 표현 미확인 |
| proposal에서 어느 정도 분량으로 작성해야 하는지 | 자료에서 직접 확인되지 않음. 다만 현재 `Final Project Proposal.docx`는 MCP Plan, Threat Model, USAGE_LOG example을 짧은 paragraph 형태로 포함함 | `Final Project Proposal.docx` |

현재 구현 기준으로는 `research_vault_agent`가 3개 tool을 노출한다.

| 현재 tool | input schema | side effect |
|---|---|---|
| `search_project_memory` | `query: string`, `limit: integer` | 없음 |
| `export_certificate_payloads` | `limit: integer` | `evidence/certificate_payloads_latest.json` write |
| `blockchain_read` | `action: enum(config/latest_block/balance/transaction)`, optional `address`, optional `tx_hash` | 없음 |

## 5. Threat Model 요구사항

### 각 server가 무엇을 read/write 해야 하는가?

| Server / Tool | Read | Write | 근거 |
|---|---|---|---|
| Filesystem MCP Server | raw files, Obsidian vault | Markdown pages | `Final Project Proposal.docx` |
| Fetch MCP Server | user-provided web URLs | 직접 확인되지 않음 | `Final Project Proposal.docx` |
| Git MCP Server | generated wiki pages/logs/version history | 직접 확인되지 않음 | `Final Project Proposal.docx` |
| `WikiKnowledgeServer.create_wiki_page` | title/content/vault path input | Obsidian Markdown page | `Final Project Proposal.docx` |
| `WikiKnowledgeServer.generate_cross_links` | page path/vault path | Markdown cross-links | `Final Project Proposal.docx` |
| `WikiKnowledgeServer.log_page_hash` | page path/agent id/page hash 대상 | hash log 또는 WorldLand metadata | `Final Project Proposal.docx` |
| Current `research_vault_agent.search_project_memory` | generated notes, daily logs, run summaries | 없음 | `mcp_servers/research_vault_agent.py` |
| Current `research_vault_agent.export_certificate_payloads` | latest summary/certificate payload data | local evidence JSON | `mcp_servers/research_vault_agent.py` |
| Current `research_vault_agent.blockchain_read` | network config/latest block/balance/transaction | 없음 | `mcp_servers/research_vault_agent.py` |
| WorldLand certificate action | page hash, cert hash, score metadata | on-chain certificate metadata | slide 12 |
| WLC payment action | accepted finding/payment target | mock/real WLC payment | slide 11, 13 |

### credential은 어디에 저장해야 하는가?

- Proposal: API keys 또는 wallet keys는 local environment variables에 저장하고 GitHub에서 제외해야 함.
- PPT slide 13: `.env`는 commit하지 않음, private keys는 environment variables에서만 읽음, wallet key는 절대 출력하지 않음.
- 현재 threat model: optional API credentials와 blockchain wallet credentials는 environment variables에서 가져옴.

### prompt injection 또는 injected description은 어떤 위험을 만들 수 있는가?

- Proposal: web content may contain prompt injection, so imported text must be treated as untrusted data, not executable instructions.
- 현재 threat model: user-provided PDFs도 untrusted text로 취급해야 하며, paper text가 agent에게 명령하려는 prompt injection을 포함할 수 있음.
- 가능한 위험:
  - imported paper/web text가 agent에게 private key 출력, external send, malicious write를 지시할 수 있음.
  - generated wiki page에 hallucinated claim이 검증 없이 들어갈 수 있음.
  - FAIL page가 실수로 certificate를 받거나 WorldLand에 기록될 수 있음.
  - mock tx가 real tx처럼 오해될 수 있음.

PPT에서 “prompt injection”이라는 단어 자체는 직접 확인되지 않음. PPT는 broader threat controls로 local content, secret handling, FAIL -> SKIP_CHAIN, mock tx prefix, real payment approval을 제시한다. 근거: slide 13.

### proposal에는 어느 정도 길이로 써야 하는가?

자료에서 직접 확인되지 않음. 현재 proposal 문서에서는 Threat Model을 한 paragraph로 작성했고, 포함 내용은 filesystem destructive edit approval, web prompt injection, env-var credential storage, WorldLand에는 hash/metadata만 저장한다는 수준이다.

## 6. USAGE_LOG.md 요구사항

### PPT/자료에서 확인되는 내용

- PPT slide 4: `USAGE_LOG`는 “Memory / Record” 계층에 포함된다.
- Proposal: MVP demo에서 agents가 Obsidian wiki page를 만들고, related note와 link를 만들고, `USAGE_LOG.md`에 entry를 쓰고, WorldLand에 page hash를 제출한다고 설명한다.
- Proposal example: `2026-05-25 | WikiCuratorAgent | create_wiki_page | input: raw/llm_wiki_note.md | output: wiki/LLM_Wiki.md | WorldLand: page_hash logged`.
- 현재 `usage_log/USAGE_LOG.md` 형식: `Date`, `Timestamp`, `User identity`, `Channel`, `Task type`, `MCP/server component`, `Action`, `Outcome`, `Latency`.
- 현재 `usage_log/TOOL_CALL_LOG.jsonl`은 MCP tool call channel, task type, tool, args summary, status, latency, result summary를 기록한다.

### final project proposal에 넣을 수 있는 예시 로그

```markdown
| Date | Timestamp | User identity | Channel | Task type | MCP/server component | Action | Outcome | Latency |
|---|---|---|---|---|---|---|---|---|
| 2026-06-08 | 2026-06-08T21:30:00+09:00 | cheon | local CLI + MCP | wiki_update | Filesystem MCP, WikiKnowledgeServer, mock-worldland-registry | Imported `raw/worldland_note.md`, created `Obsidian/WorldLand_Knowledge_Wiki.md`, generated 3 cross-links, computed `page_hash`, and recorded mock certificate payload. | Wiki page created; cross-links added; `page_hash` logged; no real WorldLand tx; mock certificate only. | 2.4s |
```

## 7. 내 프로젝트에 적용: WorldLand Knowledge Wiki Agent

| MCP Server / Tool | 내 프로젝트에서의 역할 | MVP에서 실제 구현 여부 | Mock 가능 여부 | 위험 요소 |
|---|---|---|---|---|
| Filesystem MCP Server | raw Markdown/PDF를 읽고 Obsidian Markdown wiki page를 저장 | 부분 구현. pipeline과 local file modules는 존재하지만 standard external MCP filesystem server 운영은 future work | 가능 | destructive edit, path traversal, private notes over-read |
| Fetch MCP Server | user-provided URL/paper metadata import | 현재 제출에서는 future work에 가까움 | 가능 | prompt injection, malicious webpage, external data leakage |
| Git MCP Server | generated wiki/log 변경 이력 추적 | 현재 workspace는 git repo가 아니므로 미구현 | 가능 | unintended commit, secret commit, history exposure |
| Custom `WikiKnowledgeServer` | original proposal의 custom server: wiki page 생성, cross-link 생성, page hash logging | proposal에는 있음. 현재 구현 이름/도구는 `research_vault_agent`로 변경 | 가능 | local write, bad links, unverified page hash logging |
| Custom `research_vault_agent.search_project_memory` | generated notes/log/evidence 검색 | 구현됨 | 불필요. read-only | private research notes 노출 |
| Custom `research_vault_agent.export_certificate_payloads` | PASS page의 `certifyPage` payload를 local evidence로 export | 구현됨 | 가능. 실제 tx 없이 payload만 생성 | payload를 real tx로 오해, wrong certificate payload |
| Custom `research_vault_agent.blockchain_read` | WorldLand/EVM config, latest block, balance, tx read | 구현됨 | 가능 | RPC endpoint leakage, user address privacy |
| EvalAgent / verifier tool | claim groundedness 평가 후 PASS/FAIL gate 적용 | 구현됨 | 가능 | hallucination, false PASS, unsupported claim acceptance |
| Obsidian wiki record | research graph와 Markdown page 저장 | 구현됨 | 가능 | private note exposure, incorrect cross-links |
| USAGE_LOG / TOOL_CALL_LOG | daily usage, MCP call, run evidence 기록 | 구현됨 | 가능 | fabricated logs, sensitive args in logs |
| WorldLand `certifyPage` action | 검증 통과 page의 page hash/cert metadata 기록 | 현재 mock/payload 중심. real tx는 future work | 가능 | accidental real tx, private key leakage, FAIL page certification |
| Mock/real WLC payment | accepted EvalAgent finding reward flow | mock payment 구현 | 가능 | real payment 실수, reward incentive distortion |

## 8. 최종 요약: Proposal용 MCP Plan 문단

The project will use MCP as a controlled tool layer between the AI agents and external resources. A filesystem tool will read local source files and write generated Markdown pages inside the Obsidian vault, while fetch and git tools can be used for user-approved web imports and version tracking. The custom MCP server, currently implemented as `research_vault_agent`, exposes project-specific tools for searching project memory, exporting certificate payloads, and reading WorldLand/EVM state without private keys. Risky actions are separated from read-only tools: real WorldLand publication, real WLC payment, external LLM calls on sensitive documents, and historical log edits require explicit human approval. Private PDFs and wiki content stay local; only page hashes, certificate hashes, and minimal verification metadata are prepared for the blockchain registry.
