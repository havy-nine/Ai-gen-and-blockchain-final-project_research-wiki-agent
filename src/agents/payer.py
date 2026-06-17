from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from typing import Any

from src.text_sanitize import sanitize_text


class PayAgent:
    def __init__(self, mock_payment: bool = True, reward_per_finding: float = 0.01):
        self.mock_payment = mock_payment
        self.reward_per_finding = reward_per_finding
        self.payments: list[dict[str, object]] = []

    def reward_accepted_findings(self, certs: list[dict[str, Any]]) -> list[dict[str, object]]:
        payments: list[dict[str, object]] = []
        for cert in certs:
            findings = cert.get("claim_checks", [])
            if not isinstance(findings, list):
                continue
            for finding in findings:
                if not isinstance(finding, dict) or finding.get("curator_decision") != "ACCEPT":
                    continue
                payments.append(self._pay(cert, finding))
        self.payments.extend(payments)
        return payments

    def _pay(self, cert: dict[str, Any], finding: dict[str, Any]) -> dict[str, object]:
        if not self.mock_payment:
            if not os.getenv("WALLET_PRIVATE_KEY"):
                raise RuntimeError("Real payment requested without WALLET_PRIVATE_KEY. Explicit confirmation and configured wallet are required.")
            raise RuntimeError("Real WLC payment is not sent by demo code. Use --mock-payment unless extending integration explicitly.")
        seed = sanitize_text(f"{cert['cert_id']}:{finding['finding_id']}:{datetime.now(timezone.utc).isoformat()}")
        return {"tx_hash": "0xmock_pay_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:48], "finding_id": finding["finding_id"], "page_id": cert["page_id"], "page_title": sanitize_text(str(cert["page_title"])), "amount_wlc": self.reward_per_finding, "reason": "accepted EvalAgent finding", "timestamp": datetime.now(timezone.utc).isoformat()}
