# Project Report

## 개요

WorldLand Knowledge Wiki Agent는 연구자가 논문 PDF를 추가하면 source-grounded wiki page와 Obsidian vault를 만들고, EvalAgent 검증을 통과한 page만 blockchain certificate 대상으로 보내는 GIST GenAI & Blockchain final project입니다.

## 문제

LLM은 논문 요약을 빠르게 만들 수 있지만, 논문에 없는 주장을 자연스럽게 섞을 수 있습니다. 연구 노트에 hallucination이 들어가면 나중에 citation, survey, 실험 설계가 모두 오염됩니다.

## 해결 방식

1. PDF/Markdown/Text source를 chunk로 분해합니다.
2. WikiCuratorAgent가 page, claim, cross-link 후보를 만듭니다.
3. EvalAgent가 source text 기준으로 claim verdict를 계산합니다.
4. `score_bps >= threshold_bps`이고 critical unsupported claim이 없으면 PASS입니다.
5. PASS page만 certificate 대상이 됩니다.
6. FAIL page는 local-only로 남고 chain action은 `SKIP_CHAIN`입니다.
7. PayAgent는 accepted EvalAgent finding에만 mock WLC를 지급합니다.

## 최신 결과

| 항목 | 값 |
|---|---:|
| run_id | `run_20260607_104835` |
| source files | 109 |
| chunks | 1328 |
| pages | 110 |
| PASS | 109 |
| FAIL | 1 |
| mock certificates | 109 |
| mock payments | 545 |

## Blockchain 설계

`contracts/PageCertificateRegistry.sol`은 certificate-only registry입니다. FAIL event를 chain에 남기는 대신, FAIL은 local log에만 남깁니다. 이 설계는 “검증된 지식만 공개 인증한다”는 프로젝트 목적과 맞습니다.

## 검증 증거

- PASS: `0xmock_cert_da5400307d8706a0803cc7c499b507a52e7b6c120740df7c`
- FAIL: `Hallucinated Failure Fixture`, `SKIP_CHAIN`, `tx_hash=None`
- Threshold: `evidence/threshold_curve.csv`, `evidence/threshold_curve.png`
- Reward: `evidence/reward_comparison.csv`, `evidence/reward_comparison.png`

## 한계와 향후 작업

현재 실제 WorldLand tx와 실제 WLC payment는 없습니다. 다음 단계는 WorldLand RPC 설정, faucet으로 test WLC 수령, contract deploy, read-only tx receipt 검증, 그리고 explicit confirmation을 거친 제한적 real payment demo입니다.
