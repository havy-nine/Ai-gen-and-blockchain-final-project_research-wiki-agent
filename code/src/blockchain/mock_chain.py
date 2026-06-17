from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from src.text_sanitize import sanitize_text


class MockBlockchain:
    def __init__(self):
        self.certificates: list[dict[str, object]] = []

    def certify_page(self, page: dict[str, object], cert: dict[str, object]) -> dict[str, object]:
        seed = sanitize_text(f"{page['page_id']}:{cert['cert_id']}:{cert['score_bps']}:{datetime.now(timezone.utc).isoformat()}")
        tx_hash = "0xmock_cert_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:48]
        cert_id = sanitize_text(str(cert["cert_id"]))
        record = {"tx_hash": tx_hash, "page_id": page["page_id"], "page_title": sanitize_text(str(page["title"])), "score_bps": cert["score_bps"], "threshold_bps": cert["threshold_bps"], "cert_hash": hashlib.sha256(cert_id.encode("utf-8")).hexdigest(), "timestamp": datetime.now(timezone.utc).isoformat()}
        self.certificates.append(record)
        return record
