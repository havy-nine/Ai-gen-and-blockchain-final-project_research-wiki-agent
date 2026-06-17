# WorldLand Real Chain Setup

이 문서는 mock certificate를 실제 WorldLand-compatible EVM transaction으로 전환하기 위한 로컬 설정 절차입니다.

## 현재 구현 상태

- `--mock-chain`: 기존처럼 `0xmock_cert_...` mock certificate를 생성합니다.
- `--real-chain`: `src/blockchain/contract.py`가 `PageCertificateRegistry.certifyPage(...)` real transaction을 전송합니다.
- 실제 WLC payment는 아직 보내지 않습니다. 처음 연결할 때는 반드시 `--mock-payment`를 유지하세요.

## 사용자가 준비해야 하는 것

1. WorldLand RPC URL
2. WorldLand chain ID
3. WorldLand explorer URL, 있으면 선택 입력
4. 새 테스트 지갑 주소
5. faucet 또는 요청받은 test WLC
6. 배포된 `PageCertificateRegistry` contract address
7. 로컬 `.env`에 직접 넣을 wallet private key

중요: private key는 채팅, Notion, Git, 스크린샷, 발표자료에 절대 넣지 마세요. 제가 필요한 것은 공개 가능한 wallet address, RPC URL, chain ID, explorer URL, contract address입니다. private key는 사용자가 직접 로컬 `.env`에 넣어야 합니다.

## .env 예시

```env
WORLDLAND_NETWORK_NAME=WorldLand Test Network
WORLDLAND_RPC_URL=https://...
WORLDLAND_CHAIN_ID=...
WORLDLAND_CURRENCY_SYMBOL=WLC
WORLDLAND_BLOCK_EXPLORER_URL=https://...
WORLDLAND_CONTRACT_ADDRESS=0x...
WALLET_PRIVATE_KEY=사용자 로컬에만 입력
EVAL_AGENT_ADDRESS=0x0000000000000000000000000000000000000001
```

## Contract 배포

`contracts/PageCertificateRegistry.sol`을 WorldLand-compatible EVM 네트워크에 배포합니다. Remix를 쓰는 경우:

1. MetaMask에 WorldLand network 추가
2. test wallet에 WLC 입금 확인
3. Remix에서 `Injected Provider - MetaMask` 선택
4. `PageCertificateRegistry.sol` 컴파일
5. Deploy
6. 배포된 contract address를 `.env`의 `WORLDLAND_CONTRACT_ADDRESS`에 저장

## 실제 certificate tx 실행

처음에는 payment를 mock으로 유지합니다.

```bash
python demo/demo_pipeline.py   --threshold-bps 7800   --llm-provider mock   --real-chain   --mock-payment   --append-usage-log
```

성공하면 `usage_log/CERTIFICATE_LOG.md`와 `usage_log/RUN_LOG.jsonl`에 실제 tx hash가 기록됩니다. explorer URL을 설정했다면 result의 `explorer_url`에도 링크가 들어갑니다.

## 안전 원칙

- FAIL page는 계속 `SKIP_CHAIN`, `tx_hash=None`입니다.
- PASS page만 `certifyPage(...)`로 전송합니다.
- 실제 WLC payment는 아직 구현하지 않았습니다.
- private key는 절대 출력하지 않습니다.
- 발표 전에는 실제 tx와 mock tx를 명확히 구분하세요.
