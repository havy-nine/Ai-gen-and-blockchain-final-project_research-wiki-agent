# Threat Model

## 보호해야 할 것

- 개인 연구 vault와 논문 메모
- 생성된 claim의 출처 근거성
- certification log의 무결성
- wallet private key와 WLC 잔액

## 주요 위협

- LLM hallucination이 검증 없이 지식 페이지로 게시되는 위험
- FAIL 페이지가 실수로 chain certificate를 받는 위험
- mock tx를 실제 WorldLand tx처럼 발표하는 위험
- private key가 로그나 PPT에 노출되는 위험
- 보상이 page 통과 자체에 지급되어 검증 기여와 무관해지는 위험

## 완화책

- `score_bps >= threshold_bps`와 critical unsupported claim 차단을 동시에 적용합니다.
- FAIL 페이지는 `SKIP_CHAIN`, `tx_hash=None`으로 남기고 blockchain call을 하지 않습니다.
- 모든 mock tx는 `0xmock_cert_`, `0xmock_pay_` prefix를 사용합니다.
- `PayAgent`는 page PASS가 아니라 accepted EvalAgent finding에만 보상합니다.
- real payment는 demo code에서 막혀 있고, private key가 없으면 즉시 실패합니다.
