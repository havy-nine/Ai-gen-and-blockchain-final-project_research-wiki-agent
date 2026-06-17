# PPT Info For ChatGPT

## 제목

WorldLand Knowledge Wiki Agent: 출처 검증 기반 논문 지식 그래프와 Blockchain Certificate Registry

## Motivation / Goal

- Motivation: 학회 논문을 한 번에 받으면 수동 분류와 신뢰도 판단이 병목이 됩니다.
- Goal: AI Agent 논문들을 자동 분류하고 신뢰도 및 근거 기반 평가를 수행하여 검증된 연구 지식 베이스를 구축합니다.
- Obsidian은 분야별 research graph이고, WorldLand는 검증 통과 page의 certificate registry입니다.

## 발표에서 먼저 말할 안전한 framing

- 현재 데모는 Ollama local LLM을 기본으로 요청합니다.
- 실제 WorldLand tx와 실제 WLC payment는 아직 없습니다.
- 대규모 batch의 실제 source-derived page들은 Ollama가 꺼지면 deterministic fallback 특성상 대부분 `score_bps=10000`으로 처리됩니다.
- 그래서 발표에서는 작은 evaluation fixture로 PASS/FAIL 다양성과 threshold trade-off를 먼저 보여주고, 109개 대규모 batch는 scalability/practicality evidence로만 보여줍니다.
- reward 실험은 EvalAgent 품질 향상을 증명하는 그래프가 아니라, accepted finding에 대해서만 mock payment가 활성화되는 reward-flow 증거입니다.

## 60초 발표 스크립트

저는 학회/워크숍 AI Agent 논문 묶음을 한 번에 받아 연구 분야별로 자동 분류하고, 근거 기반 신뢰도 평가를 수행해 검증된 Obsidian 연구 지식 베이스를 만드는 Agent를 만들었습니다. PDF를 chunk로 나누고 WikiCuratorAgent가 page와 claim을 생성한 뒤, EvalAgent가 각 claim이 source text에 의해 supported 되는지 검증합니다. 현재 대규모 batch는 재현 가능한 `mock` evaluator로 pipeline을 검증했기 때문에 실제 source-derived page는 대부분 full-supported로 처리됩니다. 그래서 publication gate의 동작은 별도 sample fixture와 hallucinated failure fixture로 보여줍니다. 기준은 `score_bps >= 7800`이고 critical unsupported claim이 있으면 FAIL입니다. PASS page만 certificate 대상으로 가고, FAIL page는 `SKIP_CHAIN`, `tx_hash=None`으로 local-only 처리됩니다. 최신 large batch는 `109`개 source file, `1328`개 chunk, `110`개 page에서 `109 PASS / 1 FAIL`, mock certificate `109`개, mock payment `545`개를 생성했습니다. 실제 WorldLand tx와 실제 WLC payment는 없습니다.

## 발표 순서 추천

1. 작은 sample fixture 먼저 보여주기: `3 PASS / 3 FAIL`, 점수 다양성 있음.
2. FAIL local-only 증거 보여주기: `SKIP_CHAIN`, `tx_hash=None`.
3. Threshold graph 보여주기: threshold가 올라가면 certified sample pages가 줄고 unsupported accepted rate가 낮아짐.
4. Large batch 보여주기: 109 source file을 분야별로 분류한 scalability evidence.
5. Reward graph 보여주기: quality improvement가 아니라 accepted-finding payment flow 증거라고 설명.
6. WorldLand 상태 정직하게 말하기: 현재 real tx 없음, mock mode.

## 핵심 수치

| 항목 | 값 |
|---|---:|
| run_id | `run_20260607_104835` |
| source files | 109 |
| chunks | 1328 |
| fixture chunks | 1 |
| pages | 110 |
| large batch PASS | 109 |
| large batch FAIL | 1 |
| threshold_bps | 7800 |
| mock certificates | 109 |
| mock payments | 545 |
| LLM provider requested | `ollama` |

## Sample evaluation fixture

| sample_id | score_bps | critical | decision_at_7800 | unsupported_accepted |
|---|---:|---|---|---:|
| sample_supported_strong | 9200 | False | PASS | 0 |
| sample_supported_good | 8700 | False | PASS | 0 |
| sample_supported_borderline | 8100 | False | PASS | 0 |
| sample_partial_below_gate | 7600 | False | FAIL | 1 |
| sample_weak_below_gate | 7200 | False | FAIL | 1 |
| sample_critical_hallucination | 0 | True | FAIL | 3 |

## PASS 예시

- page: `3D Diffuser Actor: Policy Diffusion with 3D Scene Representations`
- tx_hash: `0xmock_cert_da5400307d8706a0803cc7c499b507a52e7b6c120740df7c`
- cert_hash: `373f954f58ef7ba21c5c3d63b451d5fe3e57938935af766205b3e15960f6c0dc`
- score_bps: `10000`
- 설명: 이 tx는 mock certificate입니다. 실제 WorldLand tx가 아닙니다.

## FAIL 예시

- page: `Hallucinated Failure Fixture`
- action: `SKIP_CHAIN`
- tx_hash: `None`
- score_bps: `0`
- critical unsupported claim: `True`
- 설명: FAIL page는 local-only이며 certificate tx를 만들지 않습니다.

## Threshold trade-off 표

| threshold_bps | large_batch_real_passed | large_batch_real_failed | sample_fixture_pages | sample_certified_pages | sample_failed_pages | unsupported_accepted_rate_pct |
|---:|---:|---:|---:|---:|---:|---:|
| 6000 | 109 | 0 | 6 | 5 | 1 | 40.0 |
| 7000 | 109 | 0 | 6 | 5 | 1 | 40.0 |
| 7800 | 109 | 0 | 6 | 3 | 3 | 0.0 |
| 8500 | 109 | 0 | 6 | 2 | 4 | 0.0 |
| 9000 | 109 | 0 | 6 | 1 | 5 | 0.0 |

## Reward policy 표

| policy | claim_checks | unsupported_caught | accepted_findings | payments | total_mock_wlc | claim |
|---|---:|---:|---:|---:|---:|---|
| no_reward_baseline | 545 | 0 | 545 | 0 | 0.0 | baseline evaluation output; no payment flow activated |
| accepted_finding_rewards | 545 | 0 | 545 | 545 | 5.45 | same mock evaluation output; accepted-finding payment flow activated |

## 절대 강하게 말하지 말 것

- 실제 WorldLand에 올렸다고 말하지 않기.
- 실제 WLC를 지급했다고 말하지 않기.
- mock evaluator가 모든 논문을 완전히 검증했다고 말하지 않기.
- reward가 실제 EvalAgent 품질을 크게 향상시켰다고 말하지 않기.

## 안전한 표현

- “현재는 Ollama local LLM을 기본 요청하고, 필요 시 deterministic fallback으로 publication gate를 재현 가능하게 검증했습니다.”
- “실제 source-derived batch는 scalability evidence이고, gate behavior는 fixture로 보여줍니다.”
- “Reward graph는 accepted-finding payment flow를 보여줍니다.”
- “실제 WorldLand/WLC 연동은 인터페이스를 분리해 두었고, tx hash는 아직 없습니다.”

## 사용할 이미지와 파일

- `images/threshold_curve.png`
- `images/reward_comparison.png`
- `sample_evaluation_fixtures.csv`
- `log_evidence/CERTIFICATE_LOG.md`
- `log_evidence/EVALUATION_LOG.md`
- `log_evidence/PAYMENT_LOG.md`
