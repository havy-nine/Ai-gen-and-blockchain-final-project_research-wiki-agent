# Workflow Diagram

```text
User PDFs in data/sources/
        |
        v
PDF/MD/TXT Chunker
        |
        v
WikiCuratorAgent
        |  creates wiki pages, claims, cross-link candidates
        v
EvalAgent
        |  score_bps >= threshold_bps and no critical unsupported claim?
        |
        +-- PASS --> certificate payload --> MockBlockchain / PageCertificateRegistry style log
        |             --> CERTIFICATE_LOG.md: CERTIFIED
        |             --> PayAgent rewards accepted EvalAgent findings
        |
        +-- FAIL --> local-only page
                      --> CERTIFICATE_LOG.md: SKIP_CHAIN, tx_hash=None
                      --> no certificate tx, no payment for rejected findings
```

최신 run `run_20260607_104835` 기준 결과는 `109 PASS / 1 FAIL`입니다.
