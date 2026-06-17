from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass

from src.text_sanitize import sanitize_jsonable, sanitize_text


FALLBACK_MESSAGE = "LLM unavailable; deterministic mock fallback used."


@dataclass
class LLMResponse:
    text: str
    provider_used: str
    fallback_used: bool
    issue: str = ""


class LLMClient:
    def __init__(self, provider: str | None = None):
        self.requested_provider = (provider or os.getenv("LLM_PROVIDER", "ollama")).lower()
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.issue = ""

    @property
    def provider_used(self) -> str:
        if self.requested_provider == "ollama" and self._ollama_available():
            return "ollama"
        if self.requested_provider == "openai" and os.getenv("OPENAI_API_KEY"):
            return "openai"
        return "mock"

    def generate_wiki(self, title: str, source_text: str) -> LLMResponse:
        prompt = f"""Create an Obsidian Markdown wiki page from the source only.
Title: {title}
Required sections: Summary, Key Claims, Source Evidence, Cross-link Candidates, Verification Status.
Do not invent facts. Use concise Korean.
SOURCE:
{source_text[:9000]}
"""
        return self.generate(prompt, self._mock_wiki(title, source_text))

    def evaluate_claim(self, claim: str, source_text: str) -> tuple[str, str, bool]:
        if self.provider_used == "mock":
            verdict = self._mock_verdict(claim, source_text)
            return verdict, "deterministic lexical evidence match", True
        prompt = f"""Return JSON only: {{"verdict":"SUPPORTED|PARTIAL|UNSUPPORTED","reason":"short reason"}}
Evaluate CLAIM against SOURCE only.
CLAIM: {claim}
SOURCE: {source_text[:6000]}
"""
        response = self.generate(prompt, json.dumps({"verdict": self._mock_verdict(claim, source_text), "reason": "fallback"}))
        try:
            data = json.loads(response.text.strip().strip('`'))
            verdict = str(data.get("verdict", "UNSUPPORTED")).upper()
            if verdict not in {"SUPPORTED", "PARTIAL", "UNSUPPORTED"}:
                verdict = "UNSUPPORTED"
            return verdict, str(data.get("reason", "")), response.fallback_used
        except json.JSONDecodeError:
            return self._mock_verdict(claim, source_text), FALLBACK_MESSAGE, True

    def generate(self, prompt: str, mock_text: str) -> LLMResponse:
        prompt = sanitize_text(prompt)
        mock_text = sanitize_text(mock_text)
        provider = self.provider_used
        if provider == "ollama":
            try:
                payload = {"model": self.ollama_model, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}}
                body = json.dumps(sanitize_jsonable(payload), ensure_ascii=False).encode("utf-8")
                req = urllib.request.Request(f"{self.ollama_base_url}/api/generate", data=body, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=90) as resp:
                    data = json.loads(resp.read().decode())
                response_text = sanitize_text(str(data.get("response", "")).strip())
                return LLMResponse(response_text or mock_text, "ollama", False)
            except Exception as exc:
                self.issue = f"{FALLBACK_MESSAGE} ({exc})"
                return LLMResponse(mock_text, "mock", True, self.issue)
        if provider == "openai":
            try:
                return self._generate_openai_response(prompt, mock_text)
            except Exception as exc:
                self.issue = f"{FALLBACK_MESSAGE} ({exc})"
                return LLMResponse(mock_text, "mock", True, self.issue)
        if self.requested_provider in {"ollama", "openai"}:
            self.issue = FALLBACK_MESSAGE
        return LLMResponse(mock_text, "mock", self.requested_provider != "mock", self.issue)

    def _generate_openai_response(self, prompt: str, mock_text: str) -> LLMResponse:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.issue = FALLBACK_MESSAGE
            return LLMResponse(mock_text, "mock", True, self.issue)
        prompt = sanitize_text(prompt)
        mock_text = sanitize_text(mock_text)
        body = json.dumps(sanitize_jsonable({"model": self.openai_model, "input": prompt}), ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(f"{self.openai_base_url}/responses", data=body, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
        text = sanitize_text(self._extract_openai_text(data).strip())
        return LLMResponse(text or mock_text, "openai", False)

    def _extract_openai_text(self, data: object) -> str:
        if isinstance(data, dict):
            output_text = data.get("output_text")
            if isinstance(output_text, str):
                return output_text
            parts: list[str] = []
            output = data.get("output")
            if isinstance(output, list):
                for item in output:
                    if not isinstance(item, dict):
                        continue
                    content = item.get("content")
                    if not isinstance(content, list):
                        continue
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        text = block.get("text")
                        if isinstance(text, str):
                            parts.append(text)
            if parts:
                return "\n".join(parts)
            choices = data.get("choices")
            if isinstance(choices, list) and choices:
                first = choices[0]
                if isinstance(first, dict):
                    message = first.get("message")
                    if isinstance(message, dict):
                        content = message.get("content")
                        if isinstance(content, str):
                            return content
        return ""

    def _ollama_available(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.ollama_base_url}/api/tags", timeout=3) as resp:
                data = json.loads(resp.read().decode())
            return any(m.get("name") == self.ollama_model for m in data.get("models", []))
        except Exception:
            self.issue = FALLBACK_MESSAGE
            return False

    def _mock_wiki(self, title: str, source_text: str) -> str:
        source_text = sanitize_text(source_text)
        title = sanitize_text(title)
        sentences = [s.strip() for s in source_text.replace("\n", " ").split(".") if len(s.strip()) > 30]
        claims = sentences[:5]
        evidence = "\n".join(f"- {c[:180]}" for c in claims[:4])
        key_claims = "\n".join(f"- {c[:180]}" for c in claims)
        return f"""# {title}

## Summary
{(claims[0] if claims else title)[:500]}.

## Key Claims
{key_claims}

## Source Evidence
{evidence}

## Cross-link Candidates
- To be evaluated by EvalAgent.

## Verification Status
PENDING_EVAL
"""

    def _mock_verdict(self, claim: str, source_text: str) -> str:
        import re
        claim = sanitize_text(claim)
        source_text = sanitize_text(source_text)
        words = {w.lower() for w in re.findall(r"[A-Za-z가-힣0-9]{3,}", claim)}
        src = {w.lower() for w in re.findall(r"[A-Za-z가-힣0-9]{3,}", source_text)}
        if not words:
            return "UNSUPPORTED"
        ratio = len(words & src) / len(words)
        if ratio >= 0.58:
            return "SUPPORTED"
        if ratio >= 0.32:
            return "PARTIAL"
        return "UNSUPPORTED"
