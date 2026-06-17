---
title: "RT 2 Vision Language Action Models"
type: wiki-page
generated_by: WikiCuratorAgent
---

# RT 2 Vision Language Action Models

Here is an Obsidian Markdown page based on the provided source content, with the required sections added:


### RT 2 Vision Language Action Models

## Summary
This paper explores how vision-language models trained on broad web-scale datasets can be directly incorporated into end-to-end robotic control to boost generalization and enable emergent semantic reasoning. The authors propose a simple approach of co-fine-tuning state-of-the-art vision-language models on both robotic trajectory data and Internet-scale vision-language tasks, such as visual question answering. This allows the model to output low-level robot actions alongside natural language responses.

## Key Claims
1. Vision-language models pretrained on broad web-scale datasets can be effectively incorporated into end-to-end robotic control.
2. Co-fine-tuning these models on both robotic trajectory data and Internet-scale vision-language tasks enables them to generate appropriate robot actions for a wide range of scenarios.
3. This approach leads to performant robotic policies, enabling the model to generalize well to novel objects and interpret semantically varied instructions.

## Source Evidence
- The authors use extensive evaluation (6k evaluation trials) to demonstrate that their approach leads to performant robotic policies.
- They show that RT-2 can obtain a range of emergent capabilities from Internet-scale training, including improved generalization to novel objects, the ability to interpret commands not present in robot training data, and rudimentary reasoning in response to user commands.

## Cross-link Candidates
- [[PaLM E An Embodied Multimodal Language Model]]
- [[LLaVA Visual Instruction Tuning]]
- [[CLIP Learning Transferable Visual Models]]
## Verification Status
PASS