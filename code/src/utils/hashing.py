"""SHA-256 해시 유틸리티"""

import hashlib
import json
from typing import Any

from src.text_sanitize import sanitize_jsonable, sanitize_text


def hash_content(content: str) -> str:
    """문자열의 SHA-256 해시를 반환합니다."""
    return hashlib.sha256(sanitize_text(content).encode("utf-8")).hexdigest()


def hash_dict(data: dict[str, Any]) -> str:
    """딕셔너리를 정렬된 JSON으로 직렬화 후 SHA-256 해시를 반환합니다."""
    serialized = json.dumps(sanitize_jsonable(data), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def hash_to_bytes32(hex_hash: str) -> bytes:
    """16진수 해시 문자열을 32바이트로 변환합니다."""
    return bytes.fromhex(hex_hash)


def score_to_uint256(score: float) -> int:
    """0.0~1.0 실수 점수를 uint256(×1000)으로 변환합니다."""
    return int(score * 1000)
