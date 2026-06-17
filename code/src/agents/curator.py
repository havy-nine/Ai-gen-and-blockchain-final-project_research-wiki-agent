from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.llm_client import LLMClient
from src.text_sanitize import sanitize_jsonable, sanitize_text
from src.pipeline.embedder import Embedder


class WikiCuratorAgent:
    def __init__(self, embedder: Embedder | None = None, llm_provider: str = "mock"):
        self.embedder = embedder or Embedder()
        self.llm = LLMClient(llm_provider)

    def generate_wiki_pages(self, chunks: list[dict], top_k: int = 3, min_similarity: float = 0.2) -> list[dict]:
        groups: dict[str, list[dict]] = {}
        for chunk in chunks:
            groups.setdefault(chunk["source_file"], []).append(chunk)
        pages = [self._create_page(source, group) for source, group in groups.items()]
        titles = [p["title"] for p in pages]
        texts = [p["content"] for p in pages]
        candidates = self.embedder.find_cross_link_candidates(titles, texts, top_k=top_k, min_similarity=min_similarity)
        for idx, page in enumerate(pages):
            page["cross_link_candidates"] = candidates.get(idx, [])
            page["content"] = self._inject_candidates(page["content"], page["cross_link_candidates"])
        return pages

    def _create_page(self, source_file: str, chunks: list[dict]) -> dict:
        title = self._title_from_source(source_file)
        source_text = sanitize_text("\n\n".join(f"[{c['chunk_id']}] {c['text']}" for c in chunks))
        llm_response = self.llm.generate_wiki(title, source_text)
        content = self._normalize_markdown(sanitize_text(title), sanitize_text(llm_response.text))
        claims = self._extract_key_claims(content)
        return {"page_id": str(uuid.uuid4()), "title": title, "content": content, "source_chunk_ids": [c["chunk_id"] for c in chunks], "source_file": source_file, "claims": claims, "cross_link_candidates": [], "accepted_cross_links": [], "llm_provider": llm_response.provider_used, "llm_fallback_used": llm_response.fallback_used, "llm_issue": llm_response.issue, "created_at": datetime.now(timezone.utc).isoformat()}

    def _normalize_markdown(self, title: str, body: str) -> str:
        lines = [line for line in body.splitlines() if line.strip() != "---" and not line.lower().startswith(("layout:", "description:", "source:"))]
        text = "\n".join(lines).strip()
        for section in ["Summary", "Key Claims", "Source Evidence", "Cross-link Candidates", "Verification Status"]:
            text = re.sub(rf"^#{{1,6}}\s*{re.escape(section)}\s*$", f"## {section}", text, flags=re.I | re.M)
        text = re.sub(r"^#\s+(.+)$", r"### \1", text, flags=re.M)
        text = f"# {title}\n\n{text}" if not text.startswith(f"# {title}") else text
        required = ["## Summary", "## Key Claims", "## Source Evidence", "## Cross-link Candidates", "## Verification Status"]
        for section in required:
            if section not in text:
                text += f"\n\n{section}\nPENDING"
        text = re.sub(r"## Verification Status\n.*?(?=\n## |\Z)", "## Verification Status\nPENDING_EVAL", text, flags=re.S)
        front = f"---\ntitle: \"{title}\"\ntype: wiki-page\ngenerated_by: WikiCuratorAgent\n---\n\n"
        return front + text

    def _inject_candidates(self, content: str, candidates: list[dict]) -> str:
        rows = [f"- {c.get('target_title')} (cosine={c.get('cosine_sim', 0):.3f})" for c in candidates]
        if not rows:
            rows = ["- None"]
        return re.sub(r"## Cross-link Candidates\n.*?(?=\n## |\Z)", "## Cross-link Candidates\n" + "\n".join(rows), content, flags=re.S)

    def apply_accepted_links(self, page: dict, verdicts: list[dict]) -> dict:
        accepted = [v for v in verdicts if v.get("accepted")]
        page["accepted_cross_links"] = accepted
        lines = [f"- [[{v['target_page']}]]" for v in accepted] or ["- None"]
        page["content"] = re.sub(r"## Cross-link Candidates\n.*?(?=\n## |\Z)", "## Cross-link Candidates\n" + "\n".join(lines), page["content"], flags=re.S)
        return page

    def save_wiki_pages(self, pages: list[dict], output_dir: str) -> None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for page in pages:
            stem = self._safe_filename(page["title"])
            (out / f"{stem}.md").write_text(page["content"], encoding="utf-8")
            (out / f"{stem}.meta.json").write_text(json.dumps(sanitize_jsonable({k: v for k, v in page.items() if k != "content"}), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  위키 페이지 {len(pages)}개 저장: {output_dir}")

    def _extract_key_claims(self, content: str) -> list[str]:
        m = re.search(r"## Key Claims\n(.*?)(?=\n## |\Z)", content, flags=re.S)
        if not m:
            return []
        claims = []
        for line in m.group(1).splitlines():
            line = re.sub(r"^[-*]\s*", "", line).strip()
            if len(line) > 12 and line != "PENDING":
                claims.append(line[:500])
        return claims[:8]

    def _title_from_source(self, source_file: str) -> str:
        return re.sub(r"\s+", " ", Path(source_file).stem.replace("_", " ").replace("-", " ")).strip()[:80]

    def _safe_filename(self, title: str) -> str:
        return re.sub(r"[^A-Za-z0-9가-힣]+", "_", title).strip("_")[:80] or "wiki_page"
