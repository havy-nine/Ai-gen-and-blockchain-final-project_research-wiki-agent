from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import TypeAlias, cast

KST = timezone(timedelta(hours=9))
ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "output" / "wiki"
OBSIDIAN_WORKSPACE = ROOT / "obsidian_workspace"
VAULT = OBSIDIAN_WORKSPACE / "obsidian_vault"
DAILY = VAULT / "Daily Logs"
PAGES = VAULT / "Pages"
EVIDENCE = VAULT / "Evidence"
TOPICS = VAULT / "Research Topics"
RUN_LOG = ROOT / "usage_log" / "RUN_LOG.jsonl"
MIN_SOURCE_FILES = 50
JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
RunSummary: TypeAlias = dict[str, JsonValue]


def configure_paths(wiki_dir: str, vault_dir: str, min_source_files: int) -> None:
    global WIKI, VAULT, DAILY, PAGES, EVIDENCE, TOPICS, MIN_SOURCE_FILES
    WIKI = (ROOT / wiki_dir).resolve() if not Path(wiki_dir).is_absolute() else Path(wiki_dir).resolve()
    VAULT = (ROOT / vault_dir).resolve() if not Path(vault_dir).is_absolute() else Path(vault_dir).resolve()
    DAILY = VAULT / "Daily Logs"
    PAGES = VAULT / "Pages"
    EVIDENCE = VAULT / "Evidence"
    TOPICS = VAULT / "Research Topics"
    MIN_SOURCE_FILES = min_source_files


def load_run_history() -> list[RunSummary]:
    runs: list[RunSummary] = []
    if RUN_LOG.exists():
        for line in RUN_LOG.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            runs.append(cast(RunSummary, json.loads(line)))
    if not runs:
        summaries = sorted((ROOT / "evidence").glob("run_*_summary.json"), key=lambda p: p.stat().st_mtime)
        if not summaries:
            raise RuntimeError("No run summary found. Run demo_pipeline first.")
        runs.append(cast(RunSummary, json.loads(summaries[-1].read_text(encoding="utf-8"))))
    return runs


def int_field(run: RunSummary, key: str) -> int:
    value = run.get(key, 0)
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return 0


def presentation_runs(runs: list[RunSummary]) -> list[RunSummary]:
    batch_runs = [run for run in runs if int_field(run, "source_files") >= MIN_SOURCE_FILES]
    return batch_runs or runs


def latest_summary(runs: list[RunSummary]) -> RunSummary:
    return presentation_runs(runs)[-1]


def run_date_kst(run: RunSummary) -> str:
    timestamp = str(run.get("timestamp", ""))
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        run_id = str(run.get("run_id", "run_00000000"))
        return run_id.split("_")[1] if "_" in run_id else datetime.now(KST).strftime("%Y%m%d")
    return dt.astimezone(KST).strftime("%Y_%m_%d")


def page_stems() -> list[str]:
    return sorted(p.stem for p in PAGES.glob("*.md"))


def pass_page_stems() -> list[str]:
    return [s for s in page_stems() if s != "Hallucinated_Failure_Fixture"]


def source_titles() -> list[str]:
    titles: list[str] = []
    for meta in sorted(WIKI.glob("*.meta.json")):
        data = cast(RunSummary, json.loads(meta.read_text(encoding="utf-8")))
        title = str(data.get("title", "")).strip()
        if title and title != "Hallucinated Failure Fixture":
            titles.append(title)
    return titles


def topic_rules() -> list[tuple[str, list[str]]]:
    return [
        (
            "Image and Video Segmentation",
            ["segmentation", "segment", "sam", "mask", "interactive_training", "live_interactive"],
        ),
        (
            "Object Detection",
            ["object_detection", "detection", "detector", "d2fanet", "yolo", "faster_r_cnn", "mask_r_cnn"],
        ),
        (
            "3D Reconstruction",
            ["3d", "reconstruction", "scene_reconstruction", "simrecon", "gaussian_splatting", "exact_gs", "x_ray", "x-ray", "simready"],
        ),
        (
            "Sensor Fusion and Autonomous Perception",
            ["sensor_fusion", "fusion", "lidar", "radar", "collaborative_perception", "adverse_weather", "autonomous"],
        ),
        (
            "AI Safety and Evaluation",
            ["safety", "red_teaming", "red_team", "tear", "evaluation", "benchmark", "hallucination"],
        ),
        (
            "Synthetic Data",
            ["synthetic", "synthetic_data", "fine_grained", "beyond_objects", "data_generation"],
        ),
        (
            "Robotics and Manipulation",
            ["robot", "robotics", "manipulation", "grasp", "activevla", "demofungrasp", "trajectory", "planning"],
        ),
        (
            "Multimodal AI",
            ["multimodal", "vision_language", "vision-language", "vlm", "llava", "clip", "poster", "posteriq", "large_language"],
        ),
        (
            "Generative AI",
            ["generative", "generation", "diffusion", "text_to_video", "text-to-video", "animation", "motion", "rigmo"],
        ),
        (
            "Computer Vision",
            ["vision", "image", "video", "cvpr", "classification", "recognition", "perception"],
        ),
    ]


def topic_summary() -> str:
    titles = " ".join(source_titles()).lower().replace("-", "_")
    topics: list[str] = []
    for label, keywords in topic_rules():
        if any(k in titles for k in keywords):
            topics.append(label)
    if not topics:
        return "AI research knowledge graph"
    return ", ".join(topics[:6]) + (", ..." if len(topics) > 6 else "")


def write_obsidian_config() -> None:
    obs = VAULT / ".obsidian"
    obs.mkdir(parents=True, exist_ok=True)
    _ = (obs / "app.json").write_text(json.dumps({"alwaysUpdateLinks": True, "showUnsupportedFiles": True}, indent=2), encoding="utf-8")
    graph_config = {
        "collapse-filter": False,
        "search": '-path:"Daily Logs"',
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": False,
    }
    _ = (obs / "graph.json").write_text(json.dumps(graph_config, indent=2), encoding="utf-8")


def copy_assets() -> None:
    for d in [PAGES, DAILY, EVIDENCE, TOPICS]:
        d.mkdir(parents=True, exist_ok=True)
    for p in WIKI.glob("*.md"):
        _ = shutil.copy2(p, PAGES / p.name)
    for name in ["threshold_curve.png", "reward_comparison.png", "threshold_curve.csv", "reward_comparison.csv"]:
        src = ROOT / "evidence" / name
        if src.exists():
            _ = shutil.copy2(src, EVIDENCE / name)


def rewrite_page_wikilinks() -> None:
    title_to_target: dict[str, str] = {}
    display_to_target: dict[str, str] = {}
    for meta in WIKI.glob("*.meta.json"):
        data = cast(RunSummary, json.loads(meta.read_text(encoding="utf-8")))
        stem = meta.stem.removesuffix(".meta")
        title = str(data.get("title", "")).strip()
        target = f"Pages/{stem}"
        if title:
            title_to_target[title] = target
        display_to_target[stem.replace("_", " ")] = target
    for page in PAGES.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for title, target in title_to_target.items():
            text = text.replace(f"[[{title}]]", f"[[{target}|{title}]]")

        def replace_unresolved(match: re.Match[str]) -> str:
            target = match.group(1).strip()
            label = match.group(2)
            if target.startswith(("Pages/", "Research Topics/", "Daily Logs/", "Evidence/")):
                return match.group(0)
            best = difflib.get_close_matches(target, display_to_target.keys(), n=1, cutoff=0.58)
            if not best:
                return match.group(0)
            resolved = display_to_target[best[0]]
            shown = label[1:] if label else target
            return f"[[{resolved}|{shown}]]"

        text = re.sub(r"\[\[([^\]|#!]+)(\|[^\]]+)?\]\]", replace_unresolved, text)
        _ = page.write_text(text, encoding="utf-8")



def paper_links() -> list[str]:
    return [f"[[Pages/{stem}|{stem.replace('_', ' ')}]]" for stem in pass_page_stems()]



def field_from_stem(stem: str) -> str:
    normalized = stem.lower().replace("-", "_")
    for field, keys in topic_rules():
        if any(key in normalized for key in keys):
            return field
    return "Other AI Papers"


def field_page_stem(field: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", field).strip("_")


def papers_by_field() -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for stem in pass_page_stems():
        grouped[field_from_stem(stem)].append(stem)
    return dict(sorted(grouped.items()))

def write_topic_pages() -> None:
    topic = topic_summary()
    grouped = papers_by_field()
    atlas_lines = [
        "# AI Research Atlas",
        "",
        "이 대주제 페이지는 Graph View에서 AI 전체를 하나의 중심 노드로 묶고, 각 분야 topic page를 통해 논문 페이지로 확장합니다.",
        "",
        "## Scope",
        f"- Current topic summary: {topic}",
        f"- Total paper pages: {len(pass_page_stems())}",
        "",
        "## Field Topic Pages",
    ]
    for field, stems in grouped.items():
        atlas_lines.append(f"- [[Research Topics/{field_page_stem(field)}|{field}]] ({len(stems)} papers)")
    atlas_lines += [
        "",
        "## Graph View Note",
        "- Daily Logs are generated for audit history but intentionally not linked here, so the graph stays focused on papers, topics, and evidence.",
    ]
    _ = (TOPICS / "AI Research Atlas.md").write_text("\n".join(atlas_lines) + "\n", encoding="utf-8")

    legacy_lines = [
        "# Robotics and Video Research",
        "",
        "이 페이지는 기존 로봇/비전 중심 graph demo를 보존하면서, 상위 대주제 [[Research Topics/AI Research Atlas|AI Research Atlas]]로 연결합니다.",
        "",
        "## Connected Field Pages",
    ]
    for field in ["Robotics and Agents", "Computer Vision", "Multimodal AI"]:
        if field in grouped:
            legacy_lines.append(f"- [[Research Topics/{field_page_stem(field)}|{field}]]")
    _ = (TOPICS / "Robotics and Video Research.md").write_text("\n".join(legacy_lines) + "\n", encoding="utf-8")

    for field, stems in grouped.items():
        lines = [
            f"# {field}",
            "",
            "## Parent Topic",
            "- [[Research Topics/AI Research Atlas|AI Research Atlas]]",
            "",
            "## Classification Purpose",
            "- 이 분야 page는 학회 논문 batch를 연구 주제별로 나누고, 관련 paper page를 한 곳에 모읍니다.",
            "- 각 paper page는 EvalAgent groundedness score와 PASS/FAIL evidence로 검증됩니다.",
            "",
            "## Connected Paper Pages",
        ]
        lines += [f"- [[Pages/{stem}|{stem.replace('_', ' ')}]]" for stem in stems]
        _ = (TOPICS / f"{field_page_stem(field)}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_home(runs: list[RunSummary]) -> None:
    summary = latest_summary(runs)
    topic = topic_summary()
    lines = [
        "# WorldLand Knowledge Wiki Vault",
        "",
        "이 vault는 AI 주요 분야 논문 PDF를 AI agent가 Obsidian 지식 그래프로 변환한 발표용 데모입니다.",
        "",
        "## Research Focus",
        "- Topic page: [[Research Topics/AI Research Atlas|AI Research Atlas]]",
        f"- Current topic: {topic}",
        "- Goal: conference paper batch -> field classification -> grounded reliability evaluation -> verified research knowledge base.",
        "",
        "## Goal",
        "AI Agent 논문들을 자동 분류하고 신뢰도 및 근거 기반 평가를 수행하여 검증된 연구 지식 베이스를 구축합니다.",
        "",
        "## Latest Run",
        f"- Run ID: `{summary['run_id']}`",
        f"- Source PDFs: {summary['source_files']}",
        f"- Chunks: {summary['chunks']}",
        f"- Pages: {summary['pages']}",
        f"- PASS / FAIL: {summary['passed']} / {summary['failed']}",
        f"- Threshold: `{summary['threshold_bps']}` bps",
        f"- Mock certificate tx: {summary['certificates_on_chain']}",
        f"- Mock payment tx: {summary['payments']}",
        "",
        "## Open In Obsidian",
        "Ubuntu에서는 `demo/open_obsidian_vault.sh`로 이 vault를 열고 Graph View를 확인하면 됩니다.",
        "",
        "## Paper Pages",
    ]
    lines += [f"- {link}" for link in paper_links()]
    lines += [
        "",
        "## Gate Evidence",
        "- [[Pages/Hallucinated_Failure_Fixture|FAIL_LOCAL_ONLY fixture]]: certificate tx가 없어야 하는 검증용 페이지",
        "- ![[Evidence/threshold_curve.png]]",
        "- ![[Evidence/reward_comparison.png]]",
        "",
        "## Accumulated Daily Logs",
    ]
    lines += [f"- [[Daily Logs/{p.stem}|{p.stem.replace('_', ' ')}]]" for p in sorted(DAILY.glob("*.md"))]
    _ = (VAULT / "Home.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_daily_pages(runs: list[RunSummary]) -> None:
    by_day: dict[str, list[RunSummary]] = defaultdict(list)
    for run in presentation_runs(runs):
        by_day[run_date_kst(run)].append(run)
    titles = source_titles()
    topic = topic_summary()
    for day, day_runs in sorted(by_day.items()):
        latest = day_runs[-1]
        lines = [
            f"# Daily Research Log - {day.replace('_', '-')}",
            "",
            "## Research Topic Reflected Today",
            "- Topic page: [[Research Topics/AI Research Atlas|AI Research Atlas]]",
            "- 목표: AI Agent/AI 논문 batch를 연구 분야별로 분류하고, 근거 기반 평가로 신뢰 가능한 지식 베이스를 유지합니다.",
            f"- 오늘 vault의 중심 주제는 **{topic}** 입니다.",
            "",
            "## Run Summary",
        ]
        for run in day_runs:
            lines += [
                f"- `{run['run_id']}`: PDFs {run['source_files']}, chunks {run['chunks']}, pages {run['pages']}, PASS {run['passed']}, FAIL {run['failed']}, mock cert {run['certificates_on_chain']}, mock pay {run['payments']}",
            ]
        lines += [
            "",
            "## Latest Paper Set",
        ]
        lines += [f"- {title}" for title in titles]
        lines += [
            "",
            "## Current Wiki Pages",
        ]
        lines += [f"- {link}" for link in paper_links()]
        lines += [
            "",
            "## Evidence Notes",
            "- PASS pages received mock certificate records only.",
            "- The FAIL fixture remained local-only and did not receive a certificate tx.",
            "- Payments are mock WLC rewards for accepted EvalAgent findings, not real token transfers.",
        ]
        if str(latest.get("run_id", "")) == str(latest_summary(runs).get("run_id", "")):
            lines += [
                "",
                "## What Changed In The Latest Run",
                f"- Latest run ID: `{latest['run_id']}`",
                f"- Source paper count is now {latest['source_files']}; this reflects the newly added paper set.",
                f"- The topic expanded toward {topic}.",
            ]
        _ = (DAILY / f"Daily_Research_Log_{day}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", default="output/wiki")
    parser.add_argument("--vault-dir", default="obsidian_workspace/obsidian_vault")
    parser.add_argument("--min-source-files", type=int, default=50)
    args = parser.parse_args()
    configure_paths(args.wiki_dir, args.vault_dir, args.min_source_files)
    runs = load_run_history()
    if VAULT.exists():
        shutil.rmtree(VAULT)
    copy_assets()
    rewrite_page_wikilinks()
    write_daily_pages(runs)
    write_topic_pages()
    write_home(runs)
    write_obsidian_config()
    print(f"Obsidian vault ready: {VAULT}")
    print(f"Daily logs: {len(list(DAILY.glob('Daily_Research_Log_*.md')))}")
    print(f"Latest run: {latest_summary(runs)['run_id']}")


if __name__ == "__main__":
    main()
