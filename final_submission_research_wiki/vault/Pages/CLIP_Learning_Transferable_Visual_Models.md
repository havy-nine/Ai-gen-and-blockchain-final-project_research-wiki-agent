---
title: "CLIP Learning Transferable Visual Models"
type: wiki-page
generated_by: WikiCuratorAgent
---

# CLIP Learning Transferable Visual Models

### CLIP Learning Transferable Visual Models

## Summary
This paper presents the Contrastive Language-Image Pre-training (CLIP) method, which leverages natural language supervision to learn visual models. The authors demonstrate that predicting captions for images from raw text data can be an efficient and scalable way to pre-train image representations on a dataset of 400 million (image, text) pairs collected from the internet. After pre-training, CLIP uses natural language to reference learned visual concepts or describe new ones, enabling zero-shot transfer to various downstream tasks such as OCR, action recognition in videos, geo-localization, and fine-grained object classification. The model transfers non-trivially to most tasks and often outperforms a fully supervised baseline without needing any dataset-specific training.

## Key Claims
1. Learning from raw text data can be an efficient way to pre-train image representations.
2. CLIP achieves good performance on various downstream tasks with minimal dataset-specific fine-tuning.
3. The approach is scalable, capable of handling datasets of up to 400 million (image, text) pairs.

## Source Evidence
1. **Pre-training Task**: Predicting which caption goes with which image from a dataset of 400 million (image, text) pairs collected from the internet.
2. **Performance on Datasets**: Benchmarked on over 30 different existing computer vision datasets, including OCR, action recognition in videos, geo-localization, and fine-grained object classification tasks.
3. **Transfer Performance**: The model transfers non-trivially to most tasks without needing any dataset-specific training.

## Cross-link Candidates
- [[Pages/LLaVA_Visual_Instruction_Tuning|LLaVA Visual Instruction Tuning]]
- [[Pages/RT_2_Vision_Language_Action_Models|RT 2 Vision Language Action Models]]
- [[Pages/DINOv2_Learning_Robust_Visual_Features_without_Supervision|DINOv2 Learning Robust Visual Features without Supervision]]
## Verification Status
PASS

## Research Wiki Metadata
- Source PDF: `CLIP_Learning_Transferable_Visual_Models.pdf`
- Status: [[Evaluation/Certified_PASS|Certified PASS]]
- Methods: [[Methods/Vision_Language_Models|Vision-Language Models]]
- Tasks: [[Tasks/Multimodal_Retrieval|Multimodal Retrieval]]

## Research Use
- Use this paper as a source-backed node in the local LLM research wiki.
- Add personal reading notes below after inspecting the original PDF.

## Personal Reading Notes
- 
