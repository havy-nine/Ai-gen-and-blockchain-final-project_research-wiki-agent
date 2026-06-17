from __future__ import annotations

import re
import uuid
from pathlib import Path

from src.text_sanitize import sanitize_text


def _estimate_tokens(text: str) -> int:
    return max(1, int(len(text) / 3))


def _make_chunk(text: str, source_file: str, start_line: int, source_type: str = "text") -> dict[str, object]:
    clean_text = sanitize_text(text).strip()
    lines = clean_text.split("\n")
    return {"chunk_id": f"c_{uuid.uuid4().hex[:8]}", "source_file": source_file, "source_type": source_type, "text": clean_text, "start_line": start_line, "end_line": start_line + len(lines) - 1, "token_count": _estimate_tokens(clean_text)}


def chunk_text(text: str, source_file: str, max_tokens: int = 450, source_type: str = "text") -> list[dict[str, object]]:
    text = sanitize_text(text)
    parts = re.split(r"\n(?=#{1,3}\s)|\n\s*\n", text.strip())
    chunks: list[dict[str, object]] = []
    buf: list[str] = []
    start = 1
    line_no = 1
    for part in parts:
        if not part.strip():
            continue
        candidate = "\n\n".join(buf + [part])
        if buf and _estimate_tokens(candidate) > max_tokens:
            chunks.append(_make_chunk("\n\n".join(buf), source_file, start, source_type))
            start = line_no
            buf = [part]
        else:
            buf.append(part)
        line_no += part.count("\n") + 2
    if buf:
        chunks.append(_make_chunk("\n\n".join(buf), source_file, start, source_type))
    return chunks


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        pages = []
        for idx, page in enumerate(reader.pages[:12], start=1):
            pages.append(f"# Page {idx}\n" + (page.extract_text() or ""))
        return sanitize_text("\n\n".join(pages))
    except Exception as exc:
        return f"PDF extraction failed for {path.name}: {exc}"


def load_and_chunk_sources(sources_dir: str, max_tokens: int = 450) -> list[dict[str, object]]:
    root = Path(sources_dir)
    all_chunks: list[dict[str, object]] = []
    files = sorted([p for p in root.iterdir() if p.is_file() and p.suffix.lower() in {".md", ".txt", ".pdf"}])
    print(f"  소스 파일 {len(files)}개 로드 중...")
    for p in files:
        if p.suffix.lower() == ".pdf":
            text = _read_pdf(p)
            source_type = "pdf"
        else:
            text = sanitize_text(p.read_text(encoding="utf-8", errors="ignore"))
            source_type = p.suffix.lower().lstrip(".") or "text"
        chunks = chunk_text(text, p.name, max_tokens=max_tokens, source_type=source_type)
        all_chunks.extend(chunks)
        print(f"    {p.name}: {len(chunks)}개 청크")
    return all_chunks
