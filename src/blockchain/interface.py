from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.blockchain.contract import WorldLandCertificateRegistry
from src.blockchain.mock_chain import MockBlockchain


@runtime_checkable
class BlockchainInterface(Protocol):
    def certify_page(self, page: dict, cert: dict) -> dict:
        ...


def create_blockchain_interface(mock: bool = True) -> BlockchainInterface:
    if mock:
        return MockBlockchain()
    return WorldLandCertificateRegistry()
