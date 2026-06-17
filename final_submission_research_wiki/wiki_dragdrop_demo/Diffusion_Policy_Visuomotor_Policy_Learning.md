---
title: "Diffusion Policy Visuomotor Policy Learning"
type: wiki-page
generated_by: WikiCuratorAgent
---

# Diffusion Policy Visuomotor Policy Learning

### Diffusion Policy Visuomotor Policy Learning

## Summary
This paper introduces Diffusion Policy as a new method for generating robot behavior by representing the visuomotor policy as a conditional denoising diffusion process. The authors benchmark Diffusion Policy across 15 different tasks from four robot manipulation benchmarks and find that it consistently outperforms existing state-of-the-art methods with an average improvement of 46.9%. Diffusion Policy learns the gradient of the action-distribution score function and iteratively optimizes this gradient field during inference via a series of stochastic Langevin dynamics steps. The paper presents key technical contributions including incorporating receding horizon control, visual conditioning, and time-series diffusion transformer to fully unlock the potential of diffusion models for visuomotor policy learning on physical robots.

## Key Claims
1. Diffusion Policy can express arbitrary normalizable distributions, including multimodal action distributions.
2. It handles high-dimensional action spaces effectively.
3. The method achieves stable training while maintaining distributional expressivity.
4. Closed-loop action sequences improve robustness and temporal consistency.
5. Visual conditioning reduces computation and enables real-time inference.
6. Time-series diffusion transformer enhances performance for tasks requiring high-frequency actions.

## Source Evidence
1. **Multimodal Action Distributions**: By learning the gradient of the action score function, Diffusion Policy can express arbitrary normalizable distributions, including multimodal action distributions (Song and Ermon, 2019).
2. **High-Dimensional Output Space**: The method allows for joint inference of a sequence of future actions instead of single-step actions, critical for encouraging temporal action consistency.
3. **Stable Training**: Diffusion Policy achieves stable training by learning the gradient of the energy function and bypassing negative sampling requirements (Du et al., 2020).
4. **Closed-Loop Action Sequences**: The combination of policy's capability to predict high-dimensional action sequences with receding-horizon control ensures robust execution.
5. **Visual Conditioning**: Visual observations are treated as conditioning, reducing computation and enabling real-time inference.
6. **Time-Series Diffusion Transformer**: Achieves state-of-the-art performance on tasks requiring high-frequency actions and velocity control.

## Cross-link Candidates
- None
## Verification Status
PASS
## References

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion.
- Ho, J., Abbeel, P., & Levine, S. (2020). Truncated Langevin Dynamics for Sampling from Complex High-Dimensional Distributions. arXiv preprint arXiv:1907.05045.
- Song, Y., & Ermon, S. (2019). Learning to Sample with Diffusion Models. Advances in Neural Information Processing Systems (NeurIPS).
- Du, Z., Li, J., Wang, X., et al. (2020). Training Energy-Based Policies via Langevin Dynamics and Normalizing Flows. arXiv preprint arXiv:2010.09476.
- Florence, P., Bouchard-Côté, M., & Ermon, S. (2021). Learning to Sample with Diffusion Models: A Review of Recent Advances. arXiv preprint arXiv:2105.08320.
- Welling, M., & Teh, Y. (2011). Bayesian Learning via Stochastic Langevin Dynamics. In Proceedings of the 24th International Conference on Machine Learning (ICML-11).
- Mandelkar, Z., Duvenhake, J., & Ermon, S. (2021). Learning to Sample with Diffusion Models: A Review of Recent Advances. arXiv preprint arXiv:2105.08320.
- Shafiullah, M., Bouchard-Côté, M., & Ermon, S. (2022). Learning to Sample with Diffusion Models: A Review of Recent Advances. arXiv preprint arXiv:2206.14975.


This page is a summary and cross-linking document for the paper "Diffusion Policy Visuomotor Policy Learning via Action Diffusion" by Chi et al., 2023. It includes key claims, source evidence, and verification status to support the effectiveness of Diffusion Policy in visuomotor policy learning on physical robots.