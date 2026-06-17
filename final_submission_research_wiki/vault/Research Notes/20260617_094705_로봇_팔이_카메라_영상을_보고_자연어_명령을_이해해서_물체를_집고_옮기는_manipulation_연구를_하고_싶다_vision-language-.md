---
type: research-note
created: "2026-06-17 09:47:05"
llm_provider_used: ollama
llm_fallback_used: false
---

# Research Note - 로봇 팔이 카메라 영상을 보고 자연어 명령을 이해해서 물체를 집고 옮기는 manipulation 연구를 하고 싶다. vision-language

## User Research Question
로봇 팔이 카메라 영상을 보고 자연어 명령을 이해해서 물체를 집고 옮기는 manipulation 연구를 하고 싶다. vision-language-action 모델과 diffusion policy 중 무엇을 먼저 읽어야 하나?

## Local LLM Synthesis
### Research Interpretation

**Vision-Language-Action Model**: 
- PerAct Perceiver Actor 提出的 Perceiver Transformer 可以高效地编码高维度观察（高达1百万个体素），仅使用少量的潜在向量，为学习6自由度任务中的稳健动作中心表示提供了强大的结构先验。
- RT-X 模型能够适应新的机器人、任务和环境，涵盖527种技能，来自22种不同的机器人平台。

**Diffusion Policy**: 
- Diffusion Policy 可以表达任意可归一化的分布，包括多模态的动作分布。它在高维度动作空间中表现良好，并且能够在保持分布表达能力的同时实现稳定的训练。
- CLIP 学习通用视觉模型的方法可以高效地预训练图像表示，无需特定数据集的微调。

### 相关论文支持

**PerAct Perceiver Actor for Multi Task Transformer Robotics**: 
- 提出的 Perceiver Transformer 可以处理6自由度任务中的高维度观察，并且仅需要少量的潜在向量来学习稳健的动作中心表示。
- RT-X 模型能够适应新的机器人、任务和环境，涵盖527种技能。

**Diffusion Policy Visuomotor Policy Learning**: 
- Diffusion Policy 在表达任意可归一化的分布方面表现出色，并且在高维度动作空间中表现良好。它能够在保持分布表达能力的同时实现稳定的训练。
- CLIP 学习通用视觉模型的方法可以高效地预训练图像表示，无需特定数据集的微调。

### 下一步实验想法

1. **结合Vision-Language-Action模型和Diffusion Policy**：
   - 实验设计：使用PerAct Perceiver Actor进行初始观察编码，并利用Diffusion Policy生成动作序列。
   - 目标：验证在6自由度任务中，通过将视觉信息与语言指令相结合来学习复杂操作的能力。

2. **实验数据收集**：
   - 收集更多关于机器人操作的多模态数据（图像、文本和动作）。
   - 评估模型在新环境下的泛化能力，并优化模型以适应不同背景和任务的新场景。

3. **性能比较与优化**：
   - 比较使用Vision-Language-Action模型和Diffusion Policy各自的优势，确定最佳组合策略。
   - 对模型进行微调，进一步提高其在复杂操作中的表现。

## Related Papers With Sources
- [[Pages/PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics|PerAct Perceiver Actor for Multi Task Transformer Robotics]] — source: `PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics.pdf`, similarity: `0.4801`
- [[Pages/Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models|Open X Embodiment Robotic Learning Datasets and RT X Models]] — source: `Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models.pdf`, similarity: `0.4783`
- [[Pages/RT_1_Robotics_Transformer_for_Real_World_Control|RT 1 Robotics Transformer for Real World Control]] — source: `RT_1_Robotics_Transformer_for_Real_World_Control.pdf`, similarity: `0.4757`
- [[Pages/Diffusion_Policy_Visuomotor_Policy_Learning|Diffusion Policy Visuomotor Policy Learning]] — source: `Diffusion_Policy_Visuomotor_Policy_Learning.pdf`, similarity: `0.4592`
- [[Pages/CLIP_Learning_Transferable_Visual_Models|CLIP Learning Transferable Visual Models]] — source: `CLIP_Learning_Transferable_Visual_Models.pdf`, similarity: `0.4313`

## Follow-up Reading Plan
- Open the linked paper pages and inspect Key Claims and Source Evidence.
- Add experiment notes below after reading.

## My Notes
- 
