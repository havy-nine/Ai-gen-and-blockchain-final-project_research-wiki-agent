from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from src.text_sanitize import sanitize_jsonable, sanitize_text


@dataclass
class LLMResult:
    text: str
    latency_ms: int
    model: str
    used: bool
    error: str | None = None


class OllamaClient:
    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout: int = 90,
    ):
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.timeout = timeout

    def is_available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.base_url}/api/tags", timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
            return any(m.get("name") == self.model for m in data.get("models", []))
        except Exception:
            return False

    def generate(self, prompt: str, system: str = "", temperature: float = 0.1) -> LLMResult:
        started = time.perf_counter()
        payload = {
            "model": self.model,
            "prompt": sanitize_text(prompt),
            "system": sanitize_text(system),
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": 4096,
            },
        }
        try:
            body = json.dumps(sanitize_jsonable(payload), ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            elapsed = int((time.perf_counter() - started) * 1000)
            return LLMResult(
                text=sanitize_text(str(data.get("response", "")).strip()),
                latency_ms=elapsed,
                model=self.model,
                used=True,
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeEncodeError) as exc:
            elapsed = int((time.perf_counter() - started) * 1000)
            return LLMResult("", elapsed, self.model, False, str(exc))

    def generate_json(self, prompt: str, system: str = "", temperature: float = 0.0) -> tuple[dict[str, Any] | list[Any] | None, LLMResult]:
        result = self.generate(prompt, system=system, temperature=temperature)
        if not result.used or not result.text:
            return None, result
        parsed = extract_json(result.text)
        return parsed, result


def extract_json(text: str) -> dict[str, Any] | list[Any] | None:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    candidates = re.findall(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None
