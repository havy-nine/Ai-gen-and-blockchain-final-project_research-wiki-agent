from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.llm_client import LLMClient
from src.pipeline.embedder import Embedder
from src.text_sanitize import sanitize_text

ROOT = Path(__file__).resolve().parents[1]


def slug(value: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9가-힣_-]+", "_", value.strip()).strip("_")
    return clean[:80] or "research_note"


def read_page_records(wiki_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for meta_path in sorted(wiki_dir.glob("*.meta.json")):
        stem = meta_path.stem.removesuffix(".meta")
        if stem.lower().startswith("hallucinated"):
            continue
        page_path = wiki_dir / f"{stem}.md"
        if not page_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        content = page_path.read_text(encoding="utf-8", errors="ignore")
        records.append({
            "stem": stem,
            "title": str(meta.get("title") or stem.replace("_", " ")),
            "source_file": str(meta.get("source_file") or ""),
            "claims": meta.get("claims") if isinstance(meta.get("claims"), list) else [],
            "content": sanitize_text(content),
        })
    return records


def rank_related(query: str, records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    if not records:
        return []
    texts = [query] + [f"{r['title']}\n{r['source_file']}\n{r['content'][:4000]}" for r in records]
    embedder = Embedder()
    matrix = embedder.compute_similarity_matrix(texts)
    scored: list[dict[str, Any]] = []
    for idx, record in enumerate(records, start=1):
        score = float(matrix[0][idx]) if matrix.size else 0.0
        scored.append({**record, "similarity": round(score, 4)})
    scored.sort(key=lambda item: float(item["similarity"]), reverse=True)
    return scored[:limit]


def build_llm_summary(query: str, related: list[dict[str, Any]], provider: str) -> tuple[str, str, bool]:
    context_lines = []
    for item in related:
        claims = "; ".join(str(c) for c in item.get("claims", [])[:3])
        context_lines.append(f"- {item['title']} | source={item['source_file']} | claims={claims}")
    prompt = f"""You are helping maintain a local Obsidian research wiki.
User research note:
{query}

Related paper evidence:
{chr(10).join(context_lines)}

Write concise Korean guidance with:
1. research interpretation,
2. how the related papers support it,
3. next experiment ideas.
Do not cite papers outside the provided evidence.
"""
    fallback = "\n".join([
        "### Local LLM fallback summary",
        "이 연구 메모는 아래 관련 논문들과 연결됩니다. 각 연결은 현재 vault의 paper page와 source PDF를 근거로 합니다.",
        "",
        "- 로봇 연구 주제는 policy learning, perception, multimodal grounding, manipulation evaluation으로 나누어 정리할 수 있습니다.",
        "- 아래 related papers를 먼저 읽고, method/task/dataset node로 확장하는 것이 좋습니다.",
    ])
    client = LLMClient(provider)
    response = client.generate(prompt, fallback)
    return sanitize_text(response.text), response.provider_used, response.fallback_used


def write_note(vault_dir: Path, query: str, related: list[dict[str, Any]], summary: str, provider_used: str, fallback_used: bool) -> Path:
    notes_dir = vault_dir / "Research Notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{slug(query)}.md"
    lines = [
        "---",
        "type: research-note",
        f"created: \"{now}\"",
        f"llm_provider_used: {provider_used}",
        f"llm_fallback_used: {str(fallback_used).lower()}",
        "---",
        "",
        f"# Research Note - {query[:80]}",
        "",
        "## User Research Question",
        query,
        "",
        "## Local LLM Synthesis",
        summary.strip(),
        "",
        "## Related Papers With Sources",
    ]
    for item in related:
        title = str(item["title"])
        stem = str(item["stem"])
        source = str(item["source_file"])
        sim = item.get("similarity", 0)
        lines.append(f"- [[Pages/{stem}|{title}]] — source: `{source}`, similarity: `{sim}`")
    lines += [
        "",
        "## Follow-up Reading Plan",
        "- Open the linked paper pages and inspect Key Claims and Source Evidence.",
        "- Add experiment notes below after reading.",
        "",
        "## My Notes",
        "- ",
    ]
    out = notes_dir / filename
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def update_home(vault_dir: Path, note_path: Path) -> None:
    home = vault_dir / "Home.md"
    if not home.exists():
        return
    text = home.read_text(encoding="utf-8")
    link = f"[[Research Notes/{note_path.stem}|{note_path.stem.replace('_', ' ')}]]"
    block = f"\n## Latest Research Notes\n- {link}\n"
    if "## Latest Research Notes" not in text:
        home.write_text(text.rstrip() + block, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an Obsidian research note from a natural-language query with related paper citations.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--wiki-dir", default="output/wiki_final_demo")
    parser.add_argument("--vault-dir", default="final_submission_research_wiki/vault")
    parser.add_argument("--provider", choices=["mock", "ollama", "openai"], default="ollama")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    wiki_dir = (ROOT / args.wiki_dir).resolve()
    vault_dir = (ROOT / args.vault_dir).resolve()
    records = read_page_records(wiki_dir)
    related = rank_related(sanitize_text(args.query), records, args.limit)
    summary, provider_used, fallback_used = build_llm_summary(sanitize_text(args.query), related, args.provider)
    note = write_note(vault_dir, sanitize_text(args.query), related, summary, provider_used, fallback_used)
    update_home(vault_dir, note)
    print(json.dumps({"note": str(note), "related_count": len(related), "provider_used": provider_used, "fallback_used": fallback_used}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
