from __future__ import annotations

from typing import Any


def sanitize_text(value: str) -> str:
    """Replace invalid UTF-16 surrogate code points from PDF extraction."""
    if not any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        return value
    return "".join("�" if 0xD800 <= ord(char) <= 0xDFFF else char for char in value)


def sanitize_jsonable(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, dict):
        return {sanitize_text(str(key)): sanitize_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_jsonable(item) for item in value)
    return value
