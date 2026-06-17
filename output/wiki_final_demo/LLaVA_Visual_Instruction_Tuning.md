---
title: "LLaVA Visual Instruction Tuning"
type: wiki-page
generated_by: WikiCuratorAgent
---

# LLaVA Visual Instruction Tuning

Here is the Obsidian Markdown wiki page based on the provided source text, with the required sections filled in:


### LLaVA Visual Instruction Tuning

## Summary
Instruction tuning large language models (LLMs) using machine-generated instruction-following data has been shown to improve zero-shot capabilities on new tasks. This paper presents the first attempt to use a language-only GPT-4 to generate multimodal language-image instruction-following data, introducing LLaVA: Large Language and Vision Assistant, an end-to-end trained large multimodal model that connects a vision encoder and an LLM for general-purpose visual and language understanding. The authors construct two evaluation benchmarks with diverse and challenging application-oriented tasks and demonstrate impressive multimodal chat abilities of LLaVA. Fine-tuning on Science QA achieves a new state-of-the-art accuracy.

## Key Claims
- **Multimodal Instruction-following Data**: We present a data reformation perspective to convert image-text pairs into appropriate instruction-following format using ChatGPT/GPT-4.
- **Large Multimodal Models (LMM)**: We develop an LMM by connecting the open-set visual encoder of CLIP with the language decoder Vicuna and fine-tuning it on our generated instructional vision-language data. Our empirical study validates the effectiveness of using generated data for LMM instruction-tuning, suggesting practical tips for building a general-purpose instruction-following visual agent.
- **Multimodal Instruction-following Benchmark**: We present LLaV A-Bench with two challenging benchmarks featuring diverse paired images, instructions, and detailed annotations.
- **Open-source**: We release the generated multimodal instruction data, codebase, model checkpoints, and a visual chat demo.

## Source Evidence
The paper presents Visual Instruction Tuning as an extension of instruction-tuning to the language-image multimodal space. It discusses how existing works in computer vision categorize multimodal instruction-following agents into two classes: end-to-end trained models for specific research topics versus systems that coordinate various models via LangChain/LLMs.

## Cross-link Candidates
- [[RT 2 Vision Language Action Models]]
- [[DINOv2 Learning Robust Visual Features without Supervision]]
- [[PaLM E An Embodied Multimodal Language Model]]
## Verification Status
PASS