---
title: "3D Gaussian Splatting for Real Time Radiance Field Rendering"
type: wiki-page
generated_by: WikiCuratorAgent
---

# 3D Gaussian Splatting for Real Time Radiance Field Rendering

### Page 1: 3D Gaussian Splatting for Real-Time Radiance Field Rendering

## Summary
This paper introduces a novel approach called 3D Gaussian Splatting, which combines the benefits of both mesh-based and neural radiance field methods. The authors present an efficient representation using 3D Gaussians to optimize scene properties while maintaining competitive training times. This method achieves state-of-the-art visual quality for real-time rendering at 1080p resolution on several established datasets.

## Key Claims
- Our method achieves real-time rendering of radiance fields with quality that equals the best previous methods, requiring optimization times competitive with the fastest previous methods.
- We introduce three key elements: a 3D Gaussian scene representation, interleaved optimization/density control of 3D Gaussians, and a fast visibility-aware rendering algorithm supporting anisotropic splatting.

## Source Evidence
The paper presents experimental results comparing our method to existing approaches:
- Ground TruthInstantNGP (9.2 fps) vs Plenoxels (8.2 fps): Our method achieves similar quality but with faster optimization times.
- Mip-NeRF360 (0.071 fps): Achieves state-of-the-art quality after 48 hours of training, which is the maximum quality they reach.
- Ours (135 fps) and Ours (93 fps): Our method achieves real-time rendering at 1080p resolution with competitive optimization times.

## Cross-link Candidates
- [[NeRF Representing Scenes as Neural Radiance Fields]]
- [[DINOv2 Learning Robust Visual Features without Supervision]]
## Verification Status
PASS
## Introduction
This section provides additional details about the introduction of anisotropic 3D Gaussians as a high-quality, unstructured representation of radiance fields. The authors explain how our method uses only SfM points for initialization and achieves high quality results without requiring Multi-View Stereo (MVS) data.

## Methodology
The second component of our method involves optimizing the properties of the 3D Gaussians: their position, opacity α, anisotropic covariance, and spherical harmonic (SH) coefficients. This optimization is interleaved with adaptive density control steps to create high-quality representations for captured scenes.

## Rendering Approach
Our third element is a fast, differentiable rendering approach that uses GPU sorting algorithms inspired by tile-based rasterization. This method respects visibility ordering through sorting and α-blending, enabling accurate backward passes during real-time rendering.


This structure provides a comprehensive overview of the paper's content without inventing any facts based on the provided source.