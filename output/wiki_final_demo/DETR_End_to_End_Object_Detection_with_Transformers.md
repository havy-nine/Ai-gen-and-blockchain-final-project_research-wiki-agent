---
title: "DETR End to End Object Detection with Transformers"
type: wiki-page
generated_by: WikiCuratorAgent
---

# DETR End to End Object Detection with Transformers

Here is a structured Obsidian Markdown page based on the provided source:


### DETR End to End Object Detection with Transformers

## Summary
This paper presents DEtection TRansformer (DETR), a new method that views object detection as a direct set prediction problem. It streamlines the detection pipeline by using an encoder-decoder architecture based on transformers, which eliminates the need for many hand-designed components like non-maximum suppression or anchor generation. DETR predicts all objects at once and outputs the final set of predictions in parallel, achieving comparable performance to Faster R-CNN on COCO dataset while demonstrating significant improvements on large objects.

## Key Claims
- **Direct Set Prediction**: DETR views object detection as a direct set prediction problem, simplifying the pipeline by removing surrogate tasks.
- **Transformer Architecture**: Uses an encoder-decoder architecture based on transformers for efficient and effective set predictions.
- **Bipartite Matching Loss**: Incorporates bipartite matching loss to uniquely assign predictions to ground truth objects in parallel.

## Source Evidence
- The paper references prior work on direct set prediction, bipartite matching losses, and transformer architectures.
- It demonstrates that DETR achieves comparable performance to Faster R-CNN on COCO dataset.
- DETR outperforms competitive baselines on Panoptic Segmentation task.

## Cross-link Candidates
- [[PerAct Perceiver Actor for Multi Task Transformer Robotics]]
## Verification Status
PASS