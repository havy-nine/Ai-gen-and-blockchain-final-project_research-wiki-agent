from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]

PAPERS: list[dict[str, object]] = [
    {
        "title": "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
        "filename": "Diffusion_Policy_Visuomotor_Policy_Learning.pdf",
        "url": "https://arxiv.org/pdf/2303.04137",
        "topic": "Robotics and Manipulation",
        "why": "famous robot manipulation policy paper for diffusion-based visuomotor control",
    },
    {
        "title": "RT-1: Robotics Transformer for Real-World Control at Scale",
        "filename": "RT_1_Robotics_Transformer_for_Real_World_Control.pdf",
        "url": "https://arxiv.org/pdf/2212.06817",
        "topic": "Robotics and Manipulation",
        "why": "large-scale real-world robot policy learning baseline",
    },
    {
        "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
        "filename": "RT_2_Vision_Language_Action_Models.pdf",
        "url": "https://arxiv.org/pdf/2307.15818",
        "topic": "Robotics and Manipulation",
        "why": "well-known VLA robotics paper connecting web knowledge and robot control",
    },
    {
        "title": "PerAct: Perceiver-Actor for Multi-Task Transformer Robotics",
        "filename": "PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics.pdf",
        "url": "https://arxiv.org/pdf/2209.05451",
        "topic": "Robotics and Manipulation",
        "why": "robot manipulation paper that connects 3D perception and action prediction",
    },
    {
        "title": "PaLM-E: An Embodied Multimodal Language Model",
        "filename": "PaLM_E_An_Embodied_Multimodal_Language_Model.pdf",
        "url": "https://arxiv.org/pdf/2303.03378",
        "topic": "Multimodal AI",
        "why": "famous embodied multimodal model for robot reasoning and planning",
    },
    {
        "title": "Open X-Embodiment: Robotic Learning Datasets and RT-X Models",
        "filename": "Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models.pdf",
        "url": "https://arxiv.org/pdf/2310.08864",
        "topic": "Robotics and Manipulation",
        "why": "large robotics dataset/model paper useful for demoing dataset nodes",
    },
    {
        "title": "Segment Anything",
        "filename": "Segment_Anything.pdf",
        "url": "https://arxiv.org/pdf/2304.02643",
        "topic": "Image and Video Segmentation",
        "why": "top-tier foundation model paper for segmentation and visual prompting",
    },
    {
        "title": "DETR: End-to-End Object Detection with Transformers",
        "filename": "DETR_End_to_End_Object_Detection_with_Transformers.pdf",
        "url": "https://arxiv.org/pdf/2005.12872",
        "topic": "Object Detection",
        "why": "famous transformer-based object detection paper",
    },
    {
        "title": "DINOv2: Learning Robust Visual Features without Supervision",
        "filename": "DINOv2_Learning_Robust_Visual_Features_without_Supervision.pdf",
        "url": "https://arxiv.org/pdf/2304.07193",
        "topic": "Computer Vision",
        "why": "strong self-supervised visual representation baseline",
    },
    {
        "title": "CLIP: Learning Transferable Visual Models From Natural Language Supervision",
        "filename": "CLIP_Learning_Transferable_Visual_Models.pdf",
        "url": "https://arxiv.org/pdf/2103.00020",
        "topic": "Multimodal AI",
        "why": "foundational vision-language model for multimodal retrieval and zero-shot transfer",
    },
    {
        "title": "LLaVA: Visual Instruction Tuning",
        "filename": "LLaVA_Visual_Instruction_Tuning.pdf",
        "url": "https://arxiv.org/pdf/2304.08485",
        "topic": "Multimodal AI",
        "why": "well-known multimodal assistant paper for vision-language reasoning",
    },
    {
        "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
        "filename": "NeRF_Representing_Scenes_as_Neural_Radiance_Fields.pdf",
        "url": "https://arxiv.org/pdf/2003.08934",
        "topic": "3D Reconstruction",
        "why": "foundational neural rendering and 3D scene representation paper",
    },
    {
        "title": "3D Gaussian Splatting for Real-Time Radiance Field Rendering",
        "filename": "3D_Gaussian_Splatting_for_Real_Time_Radiance_Field_Rendering.pdf",
        "url": "https://arxiv.org/pdf/2308.04079",
        "topic": "3D Reconstruction",
        "why": "famous 3D reconstruction/rendering paper useful for graph diversity",
    },
]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise RuntimeError(f"downloaded content is not a PDF: {url}")
    dest.write_bytes(data)


def copy_local_fallback(dest_dir: Path, manifest: list[dict[str, object]]) -> None:
    local_dir = ROOT / "data" / "cvpr2026_robotics_sources"
    if not local_dir.exists():
        return
    for src in sorted(local_dir.glob("*.pdf"))[:2]:
        dest = dest_dir / src.name
        if not dest.exists():
            shutil.copy2(src, dest)
            fallback_record: dict[str, object] = {
                "title": src.stem.replace("_", " "),
                "filename": dest.name,
                "url": "local:data/cvpr2026_robotics_sources/" + src.name,
                "topic": "Robotics and Manipulation",
                "why": "local fallback robotics paper for offline demo reliability",
                "status": "copied-local-fallback",
            }
            manifest.append(fallback_record)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a small famous AI/robotics paper set for the final research-wiki demo.")
    parser.add_argument("--dest-dir", default="data/final_demo_papers")
    parser.add_argument("--limit", type=int, default=len(PAPERS))
    args = parser.parse_args()

    dest_dir = (ROOT / args.dest_dir).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []

    for paper in PAPERS[: max(0, args.limit)]:
        dest = dest_dir / str(paper["filename"])
        record: dict[str, object] = dict(paper)
        try:
            if not dest.exists() or dest.stat().st_size < 1024:
                print(f"downloading: {paper['title']}")
                download(str(cast(str, paper["url"])), dest)
            record["status"] = "downloaded" if dest.exists() else "missing"
            record["bytes"] = dest.stat().st_size if dest.exists() else 0
        except Exception as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
        manifest.append(record)

    if not any(item.get("status") in {"downloaded", "copied-local-fallback"} for item in manifest):
        copy_local_fallback(dest_dir, manifest)

    manifest_path = dest_dir / "FINAL_DEMO_PAPERS_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"dest_dir": str(dest_dir), "pdf_count": len(list(dest_dir.glob("*.pdf"))), "manifest": str(manifest_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
