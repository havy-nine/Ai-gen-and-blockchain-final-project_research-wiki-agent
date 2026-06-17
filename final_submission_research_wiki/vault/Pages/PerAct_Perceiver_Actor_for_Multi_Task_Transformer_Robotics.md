---
title: "PerAct Perceiver Actor for Multi Task Transformer Robotics"
type: wiki-page
generated_by: WikiCuratorAgent
---

# PerAct Perceiver Actor for Multi Task Transformer Robotics

Here is the Obsidian Markdown page based on the provided source:


### PerAct Perceiver Actor for Multi Task Transformer Robotics

## Summary
This paper introduces PERACT (short for PERCEIVER -ACTOR), a language-conditioned behavior-cloning agent designed to learn and imitate various 6-DoF manipulation tasks. The authors investigate whether Transformers can be effectively applied to robotic manipulation by proposing a novel formulation that leverages Perceiver Transforms to encode high-dimensional observations and actions.

## Key Claims
1. **Transformer Power in Manipulation**: Transformers, despite their prevalence in NLP and CV, are not directly applicable to 6-DoF robotic manipulation due to the limited data available.
2. **Perceiver Transformer for Robotic Manipulation**: The authors propose a Perceiver Transformer that can efficiently encode high-dimensional observations (up to 1 million voxels) with only a small set of latent vectors, providing a strong structural prior for learning robust action-centric representations in 6-DoF tasks.
3. **Multi-Task Learning Efficiency**: PERACT achieves significant performance improvements over image-to-action agents and 3D ConvNet baselines by training on just a few demonstrations per task.

## Source Evidence
1. The paper presents experiments conducted in the RL-Bench environment, where PERACT is trained to perform a wide range of 6-DoF manipulation tasks with diverse variations.
2. Empirical results show that PERACT outperforms existing image-to-action agents and 3D ConvNet baselines by significant margins (up to 34× improvement).
3. The authors demonstrate the effectiveness of their approach on both simulated and real-world tasks, achieving impressive performance even when trained with minimal demonstrations.

## Cross-link Candidates
- [[Pages/RT_1_Robotics_Transformer_for_Real_World_Control|RT 1 Robotics Transformer for Real World Control]]
- [[Pages/DETR_End_to_End_Object_Detection_with_Transformers|DETR End to End Object Detection with Transformers]]
- [[Pages/RT_2_Vision_Language_Action_Models|RT 2 Vision Language Action Models]]
## Verification Status
PASS

## Research Wiki Metadata
- Source PDF: `PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics.pdf`
- Status: [[Evaluation/Certified_PASS|Certified PASS]]
- Methods: [[Methods/Perceiver_Actor|Perceiver-Actor]]
- Tasks: [[Tasks/Robot_Manipulation|Robot Manipulation]]

## Research Use
- Use this paper as a source-backed node in the local LLM research wiki.
- Add personal reading notes below after inspecting the original PDF.

## Personal Reading Notes
- 
