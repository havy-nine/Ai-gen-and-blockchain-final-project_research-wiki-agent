from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import cast

JsonDict = dict[str, object]


def network_config() -> JsonDict:
    return {
        "network_name": os.getenv("WORLDLAND_NETWORK_NAME", "WorldLand Test Network"),
        "rpc_url_configured": bool(os.getenv("WORLDLAND_RPC_URL", "")),
        "chain_id": os.getenv("WORLDLAND_CHAIN_ID", ""),
        "currency_symbol": os.getenv("WORLDLAND_CURRENCY_SYMBOL", "WLC"),
        "contract_address_configured": bool(os.getenv("WORLDLAND_CONTRACT_ADDRESS", "")),
        "private_key_required": False,
    }


def rpc_call(method: str, params: list[object] | None = None, timeout: int = 10) -> JsonDict:
    rpc_url = os.getenv("WORLDLAND_RPC_URL", "")
    if not rpc_url:
        return {"ok": False, "status": "missing_rpc_url", "method": method, "config": network_config()}
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode("utf-8")
    request = urllib.request.Request(rpc_url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = cast(JsonDict, json.loads(response.read().decode("utf-8")))
    except (urllib.error.URLError, TimeoutError) as exc:
        return {"ok": False, "status": "rpc_error", "method": method, "error": exc.__class__.__name__}
    if "error" in data:
        return {"ok": False, "status": "rpc_error", "method": method, "error": data["error"]}
    return {"ok": True, "status": "success", "method": method, "result": data.get("result")}


def get_latest_block() -> JsonDict:
    return rpc_call("eth_blockNumber")


def get_balance(address: str) -> JsonDict:
    return rpc_call("eth_getBalance", [address, "latest"])


def get_transaction(tx_hash: str) -> JsonDict:
    return rpc_call("eth_getTransactionByHash", [tx_hash])
