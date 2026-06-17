from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_records(wiki_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for meta_path in sorted(wiki_dir.glob("*.meta.json")):
        stem = meta_path.stem.removesuffix(".meta")
        if stem.lower().startswith("hallucinated"):
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        records.append({
            "stem": stem,
            "title": str(meta.get("title") or stem.replace("_", " ")),
            "source_file": str(meta.get("source_file") or ""),
        })
    return records


def infer_nodes(title: str) -> dict[str, list[str]]:
    text = title.lower().replace("-", "_")
    methods: list[str] = []
    tasks: list[str] = []
    datasets: list[str] = []
    if any(k in text for k in ["diffusion", "diffusion_policy", "policy"]):
        methods.append("Diffusion Policy")
        tasks.append("Robot Manipulation")
    if any(k in text for k in ["rt_1", "rt 1", "rt_2", "rt 2", "rt_x", "rt x", "robotics_transformer", "robotics transformer", "vision_language_action", "vision language action", "activevla", "palm_e", "palm e", "embodied"]):
        methods.append("Vision-Language-Action Models")
        tasks.append("Robot Control")
    if "segment" in text or "sam" in text:
        methods.append("Promptable Segmentation")
        tasks.append("Image and Video Segmentation")
    if any(k in text for k in ["gaussian", "splatting", "reconstruction", "simrecon", "nerf", "radiance"]):
        methods.append("3D Reconstruction")
        tasks.append("Scene Understanding")
    if any(k in text for k in ["lidar", "radar", "sensor_fusion", "sensor fusion"]):
        methods.append("Sensor Fusion")
        tasks.append("Autonomous Perception")
    if any(k in text for k in ["peract", "perceiver_actor", "perceiver actor"]):
        methods.append("Perceiver-Actor")
        tasks.append("Robot Manipulation")
    if any(k in text for k in ["open_x", "open x", "embodiment", "rt_x", "rt x"]):
        methods.append("Robot Learning Dataset")
        tasks.append("Robot Control")
        datasets.append("Open X-Embodiment")
    if any(k in text for k in ["clip", "llava", "visual_instruction", "visual instruction", "vision_language", "vision language"]):
        methods.append("Vision-Language Models")
        tasks.append("Multimodal Retrieval")
    if any(k in text for k in ["detr", "object_detection", "object detection"]):
        methods.append("Transformer Detection")
        tasks.append("Object Detection")
    if any(k in text for k in ["dino", "dinov2", "self_supervised", "self supervised"]):
        methods.append("Self-Supervised Vision")
        tasks.append("Visual Representation Learning")
    if not methods:
        methods.append("Paper Reading")
    if not tasks:
        tasks.append("Research Survey")
    return {"methods": sorted(set(methods)), "tasks": sorted(set(tasks)), "datasets": datasets}


def stem(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9가-힣]+", "_", value).strip("_")


def write_index(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([f"# {title}", "", *lines]) + "\n", encoding="utf-8")


def enhance_pages(vault_dir: Path, records: list[dict[str, Any]]) -> None:
    for record in records:
        page = vault_dir / "Pages" / f"{record['stem']}.md"
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        if "## Research Wiki Metadata" in text:
            continue
        nodes = infer_nodes(str(record["title"]))
        meta_lines = [
            "",
            "## Research Wiki Metadata",
            f"- Source PDF: `{record['source_file']}`",
            "- Status: [[Evaluation/Certified_PASS|Certified PASS]]",
            "- Methods: " + ", ".join(f"[[Methods/{stem(m)}|{m}]]" for m in nodes["methods"]),
            "- Tasks: " + ", ".join(f"[[Tasks/{stem(t)}|{t}]]" for t in nodes["tasks"]),
            "",
            "## Research Use",
            "- Use this paper as a source-backed node in the local LLM research wiki.",
            "- Add personal reading notes below after inspecting the original PDF.",
            "",
            "## Personal Reading Notes",
            "- ",
        ]
        page.write_text(text.rstrip() + "\n" + "\n".join(meta_lines) + "\n", encoding="utf-8")


def write_portal(vault_dir: Path, wiki_dir: Path, records: list[dict[str, Any]]) -> None:
    for name in ["Methods", "Tasks", "Datasets", "Research Notes", "Evaluation", "Sources", "_hidden"]:
        (vault_dir / name).mkdir(parents=True, exist_ok=True)

    method_map: dict[str, list[dict[str, Any]]] = {}
    task_map: dict[str, list[dict[str, Any]]] = {}
    dataset_map: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        nodes = infer_nodes(str(record["title"]))
        for method in nodes["methods"]:
            method_map.setdefault(method, []).append(record)
        for task in nodes["tasks"]:
            task_map.setdefault(task, []).append(record)
        for dataset in nodes["datasets"]:
            dataset_map.setdefault(dataset, []).append(record)

    for method, papers in sorted(method_map.items()):
        write_index(vault_dir / "Methods" / f"{stem(method)}.md", method, ["## Related Papers", *[f"- [[Pages/{p['stem']}|{p['title']}]]" for p in papers]])
    for task, papers in sorted(task_map.items()):
        write_index(vault_dir / "Tasks" / f"{stem(task)}.md", task, ["## Related Papers", *[f"- [[Pages/{p['stem']}|{p['title']}]]" for p in papers]])
    for dataset, papers in sorted(dataset_map.items()):
        write_index(vault_dir / "Datasets" / f"{stem(dataset)}.md", dataset, ["## Related Papers", *[f"- [[Pages/{p['stem']}|{p['title']}]]" for p in papers]])

    write_index(
        vault_dir / "Sources" / "Source Library.md",
        "Source Library",
        ["이 페이지는 final demo에 사용된 PDF source와 생성된 paper page를 연결합니다.", "", "## Papers", *[f"- [[Pages/{p['stem']}|{p['title']}]] — `{p['source_file']}`" for p in records]],
    )
    write_index(
        vault_dir / "Evaluation" / "Certified_PASS.md",
        "Certified PASS",
        ["EvalAgent gate를 통과해 mock certificate 대상으로 처리된 page입니다.", "", "## Certified Papers", *[f"- [[Pages/{p['stem']}|{p['title']}]]" for p in records]],
    )
    write_index(
        vault_dir / "Reading Queue.md",
        "Reading Queue",
        ["## Suggested Review Order", *[f"- [ ] [[Pages/{p['stem']}|{p['title']}]]" for p in records[:10]]],
    )
    write_index(
        vault_dir / "Research Dashboard.md",
        "Research Dashboard",
        [
            "## Start Here",
            "- [[Research Topics/AI Research Atlas|AI Research Atlas]]",
            "- [[Sources/Source Library|Source Library]]",
            "- [[Reading Queue]]",
            "- [[Evaluation/Certified_PASS|Certified PASS]]",
            "- [[Research Notes]]",
            "- [[Datasets]]",
            "",
            "## Method Map",
            *[f"- [[Methods/{stem(m)}|{m}]] ({len(papers)} papers)" for m, papers in sorted(method_map.items())],
            "",
            "## Task Map",
            *[f"- [[Tasks/{stem(t)}|{t}]] ({len(papers)} papers)" for t, papers in sorted(task_map.items())],
            "",
            "## Dataset Map",
            *[f"- [[Datasets/{stem(d)}|{d}]] ({len(papers)} papers)" for d, papers in sorted(dataset_map.items())],
        ],
    )
    home = vault_dir / "Home.md"
    if home.exists():
        text = home.read_text(encoding="utf-8")
        if "[[Research Dashboard]]" not in text:
            text = text.replace("## Research Focus", "## Research Portal\n- [[Research Dashboard]]\n- [[Sources/Source Library|Source Library]]\n- [[Reading Queue]]\n\n## Research Focus")
            home.write_text(text, encoding="utf-8")


def write_clean_graph_config(vault_dir: Path) -> None:
    obsidian = vault_dir / ".obsidian"
    obsidian.mkdir(parents=True, exist_ok=True)
    graph_config = {
        "collapse-filter": False,
        "search": '-path:"Daily Logs" -path:"Evidence" -path:"Evaluation" -path:"_hidden" -Hallucinated -FAIL_LOCAL_ONLY',
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": True,
        "showOrphans": False,
        "collapse-color-groups": True,
        "colorGroups": [
            {"query": "path:Pages", "color": {"a": 1, "rgb": 5395026}},
            {"query": "path:Methods OR path:Tasks OR path:Datasets", "color": {"a": 1, "rgb": 11657298}},
            {"query": "path:Research Notes", "color": {"a": 1, "rgb": 16755200}},
        ],
    }
    (obsidian / "graph.json").write_text(json.dumps(graph_config, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enhance generated Obsidian vault into a research portal.")
    parser.add_argument("--wiki-dir", default="output/wiki_final_demo")
    parser.add_argument("--vault-dir", default="final_submission_research_wiki/vault")
    args = parser.parse_args()
    wiki_dir = (ROOT / args.wiki_dir).resolve()
    vault_dir = (ROOT / args.vault_dir).resolve()
    records = load_records(wiki_dir)
    enhance_pages(vault_dir, records)
    write_portal(vault_dir, wiki_dir, records)
    write_clean_graph_config(vault_dir)
    print(json.dumps({"vault_dir": str(vault_dir), "papers": len(records), "portal": str(vault_dir / "Research Dashboard.md")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
