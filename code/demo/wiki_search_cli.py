from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline.embedder import Embedder
from src.text_sanitize import sanitize_text

ROOT = Path(__file__).resolve().parents[1]


def load_records(wiki_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for meta_path in sorted(wiki_dir.glob("*.meta.json")):
        stem = meta_path.stem.removesuffix(".meta")
        if stem.lower().startswith("hallucinated"):
            continue
        page_path = wiki_dir / f"{stem}.md"
        if not page_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        content = sanitize_text(page_path.read_text(encoding="utf-8", errors="ignore"))
        claims = meta.get("claims") if isinstance(meta.get("claims"), list) else []
        records.append({
            "stem": stem,
            "title": str(meta.get("title") or stem.replace("_", " ")),
            "source_file": str(meta.get("source_file") or ""),
            "claims": [str(c) for c in claims[:5]],
            "content": content,
        })
    return records


def lexical_search(query: str, records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    terms = [t.lower() for t in re.findall(r"[A-Za-z가-힣0-9]{2,}", query)]
    scored: list[dict[str, Any]] = []
    for record in records:
        haystack = f"{record['title']} {record['source_file']} {record['content']}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score > 0:
            scored.append({**record, "score": score})
    scored.sort(key=lambda item: int(item["score"]), reverse=True)
    return scored[:limit]


def semantic_search(query: str, records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    if not records:
        return []
    texts = [query] + [f"{r['title']}\n{r['source_file']}\n{r['content'][:4000]}" for r in records]
    embedder = Embedder()
    matrix = embedder.compute_similarity_matrix(texts)
    scored: list[dict[str, Any]] = []
    for idx, record in enumerate(records, start=1):
        similarity = float(matrix[0][idx]) if matrix.size else 0.0
        scored.append({**record, "similarity": round(similarity, 4)})
    scored.sort(key=lambda item: float(item["similarity"]), reverse=True)
    return scored[:limit]


def print_human(results: list[dict[str, Any]], mode: str) -> None:
    if not results:
        print("No related papers found.")
        return
    for idx, item in enumerate(results, start=1):
        metric = item.get("similarity") if mode == "semantic" else item.get("score")
        print(f"{idx}. {item['title']}")
        print(f"   source: {item['source_file']}")
        print(f"   {mode}: {metric}")
        print(f"   obsidian: [[Pages/{item['stem']}|{item['title']}]]")
        claims = item.get("claims", [])
        if claims:
            print(f"   claim: {claims[0]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search generated wiki pages and return related papers with source citations.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--wiki-dir", default="output/wiki_final_demo")
    parser.add_argument("--mode", choices=["semantic", "keyword"], default="semantic")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    wiki_dir = (ROOT / args.wiki_dir).resolve()
    records = load_records(wiki_dir)
    query = sanitize_text(args.query)
    results = semantic_search(query, records, args.limit) if args.mode == "semantic" else lexical_search(query, records, args.limit)
    compact = [
        {
            "title": item["title"],
            "source_file": item["source_file"],
            "obsidian_link": f"[[Pages/{item['stem']}|{item['title']}]]",
            "similarity": item.get("similarity"),
            "keyword_score": item.get("score"),
            "top_claim": item.get("claims", [""])[0] if item.get("claims") else "",
        }
        for item in results
    ]
    if args.json:
        print(json.dumps({"query": query, "mode": args.mode, "results": compact}, ensure_ascii=False, indent=2))
    else:
        print_human(results, args.mode)


if __name__ == "__main__":
    main()
