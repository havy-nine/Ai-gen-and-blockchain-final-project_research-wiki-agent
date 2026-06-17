from __future__ import annotations

import hashlib
import importlib
import json
import os
from datetime import datetime, timezone
from typing import cast

from src.text_sanitize import sanitize_jsonable, sanitize_text

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv is not None:
    _ = load_dotenv()

PAGE_CERTIFICATE_REGISTRY_ABI: list[dict[str, object]] = [
    {
        "inputs": [
            {"internalType": "string", "name": "pageId", "type": "string"},
            {"internalType": "bytes32", "name": "pageHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "certHash", "type": "bytes32"},
            {"internalType": "uint16", "name": "scoreBps", "type": "uint16"},
            {"internalType": "uint16", "name": "thresholdBps", "type": "uint16"},
            {"internalType": "address", "name": "evaluator", "type": "address"},
        ],
        "name": "certifyPage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


class WorldLandCertificateRegistry:
    def __init__(self):
        self.network_name: str = os.getenv("WORLDLAND_NETWORK_NAME", "WorldLand Test Network")
        self.rpc_url: str = os.getenv("WORLDLAND_RPC_URL", "")
        self.chain_id: str = os.getenv("WORLDLAND_CHAIN_ID", "")
        self.contract_address: str = os.getenv("WORLDLAND_CONTRACT_ADDRESS", "")
        self.block_explorer_url: str = os.getenv("WORLDLAND_BLOCK_EXPLORER_URL", "").rstrip("/")
        self.wallet_private_key: str = os.getenv("WALLET_PRIVATE_KEY", "")
        self.evaluator_address: str = os.getenv("EVAL_AGENT_ADDRESS", "0x0000000000000000000000000000000000000001")

    def configured(self) -> bool:
        return all([self.rpc_url, self.chain_id, self.contract_address, self.wallet_private_key])

    def missing_config(self) -> list[str]:
        required = {
            "WORLDLAND_RPC_URL": self.rpc_url,
            "WORLDLAND_CHAIN_ID": self.chain_id,
            "WORLDLAND_CONTRACT_ADDRESS": self.contract_address,
            "WALLET_PRIVATE_KEY": self.wallet_private_key,
        }
        return [key for key, value in required.items() if not value]

    def certify_page(self, page: dict[str, object], cert: dict[str, object]) -> dict[str, object]:
        missing = self.missing_config()
        if missing:
            raise RuntimeError(f"WorldLand config missing: {', '.join(missing)}. Use --mock-chain or set local .env.")

        try:
            web3_module = importlib.import_module("web3")
        except ImportError as exc:
            raise RuntimeError("web3 is required for --real-chain. Run: pip install -r requirements.txt") from exc

        web3_class = getattr(web3_module, "Web3")
        chain_id = int(self.chain_id)
        web3 = web3_class(web3_class.HTTPProvider(self.rpc_url))
        if not web3.is_connected():
            raise RuntimeError(f"Could not connect to {self.network_name} RPC: {self.rpc_url}")

        account = web3.eth.account.from_key(self.wallet_private_key)
        contract = web3.eth.contract(address=web3.to_checksum_address(self.contract_address), abi=PAGE_CERTIFICATE_REGISTRY_ABI)
        evaluator = web3.to_checksum_address(self.evaluator_address)
        score_bps = self._required_int(cert, "score_bps")
        threshold_bps = self._required_int(cert, "threshold_bps")
        page_hash = self._bytes32_hash(self._page_payload(page))
        cert_hash = self._bytes32_hash(self._cert_payload(cert))
        nonce = web3.eth.get_transaction_count(account.address)
        function_call = contract.functions.certifyPage(
            str(page["page_id"]),
            page_hash,
            cert_hash,
            score_bps,
            threshold_bps,
            evaluator,
        )
        tx: dict[str, object] = {
            "from": account.address,
            "nonce": nonce,
            "chainId": chain_id,
        }
        gas_price = web3.eth.gas_price
        tx["gasPrice"] = gas_price
        estimated_gas = function_call.estimate_gas({"from": account.address})
        tx["gas"] = int(estimated_gas * 1.2)
        built_tx = function_call.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(built_tx, self.wallet_private_key)
        raw_tx = getattr(signed_tx, "rawTransaction", None) or getattr(signed_tx, "raw_transaction")
        tx_hash_bytes = web3.eth.send_raw_transaction(raw_tx)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash_bytes, timeout=120)
        tx_hash = web3.to_hex(tx_hash_bytes)
        block_number = cast(int, receipt.get("blockNumber", 0))
        status = cast(int, receipt.get("status", 0))
        if status != 1:
            raise RuntimeError(f"WorldLand transaction failed: {tx_hash}")
        return {
            "tx_hash": tx_hash,
            "page_id": page["page_id"],
            "page_title": page["title"],
            "score_bps": score_bps,
            "threshold_bps": threshold_bps,
            "page_hash": "0x" + page_hash.hex(),
            "cert_hash": "0x" + cert_hash.hex(),
            "block_number": block_number,
            "chain_id": chain_id,
            "network_name": self.network_name,
            "explorer_url": self._explorer_tx_url(tx_hash),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _required_int(self, source: dict[str, object], key: str) -> int:
        value = source.get(key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise RuntimeError(f"Expected integer certificate field: {key}")
        return value

    def _page_payload(self, page: dict[str, object]) -> str:
        payload = {
            "page_id": page.get("page_id", ""),
            "title": page.get("title", ""),
            "source_file": page.get("source_file", ""),
            "content": page.get("content", ""),
        }
        return json.dumps(sanitize_jsonable(payload), ensure_ascii=False, sort_keys=True)

    def _cert_payload(self, cert: dict[str, object]) -> str:
        payload = {
            "cert_id": cert.get("cert_id", ""),
            "page_id": cert.get("page_id", ""),
            "score_bps": cert.get("score_bps", 0),
            "threshold_bps": cert.get("threshold_bps", 0),
            "has_critical_unsupported_claim": cert.get("has_critical_unsupported_claim", False),
            "evaluated_at": cert.get("evaluated_at", ""),
        }
        return json.dumps(sanitize_jsonable(payload), ensure_ascii=False, sort_keys=True)

    def _bytes32_hash(self, value: str) -> bytes:
        return hashlib.sha256(sanitize_text(value).encode("utf-8")).digest()

    def _explorer_tx_url(self, tx_hash: str) -> str:
        if not self.block_explorer_url:
            return ""
        return f"{self.block_explorer_url}/tx/{tx_hash}"
