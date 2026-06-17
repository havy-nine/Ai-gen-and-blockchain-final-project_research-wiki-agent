from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline.runner import PipelineRunner

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md"}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9가-힣_-]+", "_", value.strip()).strip("_")
    return slug[:60] or "typed_source"


def _unique_path(directory: Path, filename: str) -> Path:
    candidate = directory / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        next_candidate = directory / f"{stem}_{counter}{suffix}"
        if not next_candidate.exists():
            return next_candidate
        counter += 1


def _parse_dragged_paths(raw: str) -> list[Path]:
    return [Path(item).expanduser().resolve() for item in shlex.split(raw) if item.strip()]


def copy_source_file(path: Path, sources_dir: Path) -> Path:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        allowed = ", ".join(sorted(ALLOWED_SUFFIXES))
        raise ValueError(f"지원하지 않는 파일 형식입니다: {path.name} (지원: {allowed})")
    sources_dir.mkdir(parents=True, exist_ok=True)
    destination = _unique_path(sources_dir, path.name)
    shutil.copy2(path, destination)
    return destination


def save_text_source(title: str, text: str, sources_dir: Path) -> Path:
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("저장할 텍스트가 비어 있습니다.")
    sources_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"typed_{timestamp}_{_slug(title)}.txt"
    destination = _unique_path(sources_dir, filename)
    heading = title.strip() or "Typed Source"
    destination.write_text(f"# {heading}\n\n{clean_text}\n", encoding="utf-8")
    return destination


def read_multiline_text() -> str:
    print("텍스트를 입력하세요. 끝나면 새 줄에 /done 을 입력하세요.")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "/done":
            break
        lines.append(line)
    return "\n".join(lines)


def run_pipeline(args: argparse.Namespace, sources_dir: Path) -> dict[str, object]:
    output_dir = (_project_root() / str(args.output_dir)).resolve()
    result = PipelineRunner(
        sources_dir=str(sources_dir),
        output_dir=str(output_dir),
        threshold_bps=int(args.threshold_bps),
        llm_provider=str(args.llm_provider),
        mock_chain=bool(args.mock_chain),
        mock_payment=bool(args.mock_payment),
        append_usage_log=bool(args.append_usage_log),
        eval_provider=args.eval_provider,
    ).run()
    keys = [
        "run_id",
        "source_files",
        "chunks",
        "pages",
        "passed",
        "failed",
        "certificates_on_chain",
        "payments",
        "threshold_bps",
        "llm_provider_requested",
        "eval_provider_requested",
        "llm_provider_used",
        "fallback_message",
    ]
    summary = {key: result[key] for key in keys}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def run_research_query(args: argparse.Namespace, query: str) -> dict[str, object]:
    from research_note_cli import build_llm_summary, rank_related, read_page_records, update_home, write_note

    clean_query = query.strip()
    if not clean_query:
        raise ValueError("연구주제가 비어 있습니다.")
    wiki_dir = (_project_root() / str(args.output_dir)).resolve()
    vault_dir = (_project_root() / str(args.vault_dir)).resolve()
    records = read_page_records(wiki_dir)
    if not records:
        raise RuntimeError(f"wiki page가 없습니다. 먼저 pipeline을 실행하세요: {wiki_dir}")
    related = rank_related(clean_query, records, int(args.research_limit))
    provider = str(args.research_provider or args.llm_provider)
    summary, provider_used, fallback_used = build_llm_summary(clean_query, related, provider)
    note = write_note(vault_dir, clean_query, related, summary, provider_used, fallback_used)
    update_home(vault_dir, note)
    result: dict[str, object] = {
        "query": clean_query,
        "note": str(note),
        "provider_used": provider_used,
        "fallback_used": fallback_used,
        "related": [
            {
                "title": str(item["title"]),
                "source_file": str(item["source_file"]),
                "similarity": item.get("similarity"),
                "obsidian_link": f"[[Pages/{item['stem']}|{item['title']}]]",
            }
            for item in related
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def interactive_loop(args: argparse.Namespace, sources_dir: Path) -> None:
    print("\n=== Source Drop CLI ===")
    print(f"소스 폴더: {sources_dir}")
    print("PDF/TXT/MD 파일은 터미널에 드래그해서 경로를 붙여넣을 수 있습니다.")
    print("텍스트도 직접 입력해서 .txt source로 저장할 수 있습니다.\n")

    while True:
        print("메뉴: [1] 파일 추가  [2] 텍스트 추가  [3] pipeline 실행  [4] 종료  [5] 연구주제 입력")
        choice = input("선택: ").strip()
        if choice == "1":
            raw = input("파일 경로를 붙여넣으세요: ").strip()
            if not raw:
                print("입력된 경로가 없습니다.")
                continue
            for path in _parse_dragged_paths(raw):
                try:
                    destination = copy_source_file(path, sources_dir)
                    print(f"추가됨: {destination}")
                except Exception as exc:
                    print(f"실패: {exc}")
        elif choice == "2":
            title = input("텍스트 제목: ").strip() or "Typed Source"
            text = read_multiline_text()
            try:
                destination = save_text_source(title, text, sources_dir)
                print(f"저장됨: {destination}")
            except Exception as exc:
                print(f"실패: {exc}")
        elif choice == "3":
            run_pipeline(args, sources_dir)
        elif choice == "4":
            print("종료합니다.")
            return
        elif choice == "5":
            query = input("연구주제를 자연어로 입력하세요: ").strip()
            try:
                run_research_query(args, query)
            except Exception as exc:
                print(f"실패: {exc}")
        else:
            print("1, 2, 3, 4, 5 중에서 선택하세요.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Drag PDFs or type text into data/sources, then optionally run the pipeline.")
    parser.add_argument("--sources-dir", default="data/sources")
    parser.add_argument("--output-dir", default="output/wiki")
    parser.add_argument("--add-file", action="append", default=[])
    parser.add_argument("--add-text", default="")
    parser.add_argument("--title", default="Typed Source")
    parser.add_argument("--run-pipeline", action="store_true")
    parser.add_argument("--no-interactive", action="store_true")
    parser.add_argument("--threshold-bps", type=int, default=7800)
    parser.add_argument("--llm-provider", choices=["mock", "ollama", "openai"], default="ollama")
    parser.add_argument("--eval-provider", choices=["mock", "ollama", "openai"], default=None)
    parser.add_argument("--mock-chain", dest="mock_chain", action="store_true", default=True)
    parser.add_argument("--real-chain", dest="mock_chain", action="store_false")
    parser.add_argument("--mock-payment", dest="mock_payment", action="store_true", default=True)
    parser.add_argument("--real-payment", dest="mock_payment", action="store_false")
    parser.add_argument("--append-usage-log", action="store_true")
    parser.add_argument("--vault-dir", default="final_submission_research_wiki/vault")
    parser.add_argument("--research-query", default="")
    parser.add_argument("--research-limit", type=int, default=7)
    parser.add_argument("--research-provider", choices=["mock", "ollama", "openai"], default=None)
    args = parser.parse_args()

    root = _project_root()
    sources_dir = (root / str(args.sources_dir)).resolve()
    added: list[Path] = []

    for raw_path in args.add_file:
        for path in _parse_dragged_paths(str(raw_path)):
            destination = copy_source_file(path, sources_dir)
            added.append(destination)
            print(f"추가됨: {destination}")

    if str(args.add_text).strip():
        destination = save_text_source(str(args.title), str(args.add_text), sources_dir)
        added.append(destination)
        print(f"저장됨: {destination}")

    if args.run_pipeline:
        run_pipeline(args, sources_dir)
        return

    if str(args.research_query).strip():
        run_research_query(args, str(args.research_query))
        return

    if args.no_interactive:
        print(json.dumps({"sources_dir": str(sources_dir), "added": [str(path) for path in added]}, ensure_ascii=False, indent=2))
        return

    interactive_loop(args, sources_dir)


if __name__ == "__main__":
    main()
