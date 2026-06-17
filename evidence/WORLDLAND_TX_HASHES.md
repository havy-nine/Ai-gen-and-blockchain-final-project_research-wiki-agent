# WorldLand Tx Hashes

## 현재 상태

- 실제 WorldLand certificate tx: 없음
- 실제 WLC payment tx: 없음
- 최신 demo chain mode: mock
- 최신 demo payment mode: mock

## Mock certificate example

- tx_hash: `0xmock_cert_da5400307d8706a0803cc7c499b507a52e7b6c120740df7c`
- page_title: `3D Diffuser Actor: Policy Diffusion with 3D Scene Representations`
- score_bps: `10000`
- threshold_bps: `7800`
- cert_hash: `373f954f58ef7ba21c5c3d63b451d5fe3e57938935af766205b3e15960f6c0dc`

## FAIL local-only example

- page_title: `Hallucinated Failure Fixture`
- certificate action: `SKIP_CHAIN`
- tx_hash: `None`
- reason: score below threshold and critical unsupported claim

실제 WorldLand tx hash가 생기기 전까지는 mock tx를 실제 tx처럼 발표하지 않습니다.
