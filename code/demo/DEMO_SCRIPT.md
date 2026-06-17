# Demo Script

## 0. 한 문장 소개

이 프로젝트는 논문 PDF를 Obsidian 지식 그래프로 만들고, EvalAgent 검증을 통과한 page만 blockchain certificate 대상으로 보내는 연구용 Blockchain Agent입니다.

## 1. 먼저 한계부터 정직하게 말하기

현재 발표 데모는 Ollama local LLM을 기본으로 요청합니다. 실제 WorldLand tx와 실제 WLC payment는 없습니다. 대규모 batch의 실제 source-derived page들은 Ollama가 꺼지면 deterministic fallback 특성상 대부분 `score_bps=10000`으로 나오므로, 그 결과는 scalability evidence로 보여주고 publication gate의 민감도는 sample fixture로 설명합니다.

## 2. Sample fixture 보여주기

파일: `sample_evaluation_fixtures.csv`

핵심 메시지:

- threshold `7800`에서 sample은 `3 PASS / 3 FAIL`입니다.
- `9200`, `8700`, `8100`은 PASS입니다.
- `7600`, `7200`, `0 critical hallucination`은 FAIL입니다.

## 3. 메인 데모 실행

```bash
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider ollama --eval-provider ollama --mock-chain --mock-payment --append-usage-log
```

관찰할 것:

- source files: `109`
- chunks: `1328`
- pages: `110`
- PASS / FAIL: `109 / 1`
- certificate tx: `0xmock_cert_...`
- FAIL evidence: `SKIP_CHAIN`, `tx_hash=None`

## 4. PASS 증거

`log_evidence/CERTIFICATE_LOG.md`에서 다음 형태를 보여줍니다.

```text
CERTIFIED | 0xmock_cert_da5400307d8706a0803cc7c499b507a52e7b6c120740df7c | 3D Diffuser Actor: Policy Diffusion with 3D Scene Representations | score_bps=10000 threshold_bps=7800
```

이것은 mock certificate이며 실제 WorldLand tx가 아닙니다.

## 5. FAIL 증거

`log_evidence/CERTIFICATE_LOG.md`와 `log_evidence/EVALUATION_LOG.md`에서 다음을 보여줍니다.

```text
SKIP_CHAIN | tx_hash=None | Hallucinated Failure Fixture | score_bps=0 threshold_bps=7800 critical=True
FAIL_LOCAL_ONLY | Hallucinated Failure Fixture | score_bps=0 threshold_bps=7800 critical=True chain_action=SKIP_CHAIN
```

핵심 메시지: FAIL page는 local-only이고 blockchain call이 없습니다.

## 6. Threshold trade-off

```bash
python demo/demo_threshold_curve.py --llm-provider ollama
```

`images/threshold_curve.png`를 보여줍니다. 설명은 “threshold가 올라가면 certified sample pages가 줄고 unsupported accepted rate가 낮아진다”입니다.

## 7. Reward policy

```bash
python demo/demo_reward_ablation.py --llm-provider ollama
```

`images/reward_comparison.png`를 보여줍니다. 제목은 “Reward Policy Activates Accepted-Finding Payments”로 설명합니다. 이 그래프를 EvalAgent 품질 향상 증거라고 말하지 말고, accepted finding에만 payment가 활성화되는 flow 증거라고 말합니다.

## 8. 마지막 한계

현재 실제 WorldLand tx와 실제 WLC payment는 없습니다. 실제 WLC 연동은 명시적 확인, wallet 설정, faucet 수령 뒤 future work로 진행합니다.

## Source Drop CLI 시연

```bash
python demo/source_drop_cli.py
```

시연 순서:

1. `파일 추가`를 누르고 PDF를 터미널에 드래그해서 경로를 붙여넣습니다.
2. `텍스트 추가`를 누르고 짧은 연구 메모를 입력합니다.
3. `/done`으로 텍스트 입력을 끝냅니다.
4. 필요하면 `pipeline 실행`으로 기존 mock pipeline을 실행합니다.

이 CLI는 파일을 `data/sources/`로 복사하거나 텍스트를 `.txt` source로 저장합니다. 실제 WorldLand tx나 실제 WLC payment는 만들지 않습니다.
