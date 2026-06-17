# WorldLand / MetaMask Connection Plan

This project is safe by default: the demo uses mock certificate and payment logs. Use this guide only when you intentionally want to show how a PASS page would become a real `PageCertificateRegistry` certificate after you have a funded test wallet.

## 1. Prepare MetaMask and Faucet Funds

1. Create or select a dedicated test wallet in MetaMask. Do not use a wallet that holds valuable assets.
2. Add the WorldLand or EVM-compatible test network in MetaMask using the values from the course/faucet page:
   - Network name: `WORLDLAND_NETWORK_NAME`
   - RPC URL: `WORLDLAND_RPC_URL`
   - Chain ID: `WORLDLAND_CHAIN_ID`
   - Currency symbol: `WORLDLAND_CURRENCY_SYMBOL`
   - Block explorer URL: `WORLDLAND_BLOCK_EXPLORER_URL`
3. Request faucet tokens for that test wallet.
4. Confirm the wallet has enough test WLC/native gas before deployment.

The repository does not store faucet credentials, seed phrases, or private keys.

## 2. Deploy the Certificate Contract

Use Remix with MetaMask for the simplest class-demo path:

1. Open Remix in the browser.
2. Create `PageCertificateRegistry.sol` and paste `contracts/PageCertificateRegistry.sol`.
3. Compile with Solidity `0.8.20` or a compatible `0.8.x` compiler.
4. In Deploy & Run, choose `Injected Provider - MetaMask`.
5. Confirm MetaMask is on the WorldLand/test network.
6. Deploy `PageCertificateRegistry`.
7. Copy the deployed contract address into `.env` as `WORLDLAND_CONTRACT_ADDRESS`.

For the current final demo, do not send real certificate transactions unless you explicitly decide to do so during presentation preparation.

## 3. Export certifyPage Payloads

Generate the exact payloads that correspond to PASS pages from the latest evidence run:

```bash
python demo/export_certificate_payloads.py --limit 3
```

Output:

```text
evidence/certificate_payloads_latest.json
```

Each payload contains the arguments for:

```solidity
certifyPage(string pageId, bytes32 pageHash, bytes32 certHash, uint16 scoreBps, uint16 thresholdBps, address evaluator)
```

Use `--limit 1` for a short live demo, or omit `--limit` to export all PASS page payloads.

## 4. Optional Real Submission Boundary

A real submission requires all of the following:

- funded MetaMask wallet,
- deployed `PageCertificateRegistry` address,
- explicit approval before each transaction,
- confirmation that the page is `PASS`, not `FAIL_LOCAL_ONLY`,
- no private key printed or committed.

The normal run remains:

```bash
python demo/demo_pipeline.py --threshold-bps 7800 --llm-provider ollama --eval-provider mock --mock-chain --mock-payment --append-usage-log
```

That command does not create real WorldLand transactions.
