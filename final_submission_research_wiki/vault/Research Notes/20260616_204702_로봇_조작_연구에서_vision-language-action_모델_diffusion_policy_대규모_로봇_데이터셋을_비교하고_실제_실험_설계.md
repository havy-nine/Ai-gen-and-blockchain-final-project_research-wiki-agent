---
type: research-note
created: "2026-06-16 20:47:02"
llm_provider_used: ollama
llm_fallback_used: false
---

# Research Note - 로봇 조작 연구에서 vision-language-action 모델, diffusion policy, 대규모 로봇 데이터셋을 비교하고 실제 실험 

## User Research Question
로봇 조작 연구에서 vision-language-action 모델, diffusion policy, 대규모 로봇 데이터셋을 비교하고 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 출처와 함께 정리해줘

## Local LLM Synthesis
### 연구 해석 및 관련 논문의 지원

**로봇 조작 연구에서 vision-language-action 모델, diffusion policy, 대규모 로봇 데이터셋을 비교하고 실제 실험 설계에 어떤 논문을 먼저 읽어야 하는지 정리해보겠습니다.**

- **vision-language-action 모델**: RT_2_Vision_Language_Action_Models 논문은 vision-language 모델이 broad web-scale datasets에서 학습한 후, end-to-end 로봇 제어로 효과적으로 적용될 수 있음을 보여줍니다. 이는 vision-language-action 모델이 다양한 상황에서 적절한 로봇 행동을 생성할 수 있다는 것을 의미합니다.
- **diffusion policy**: Diffusion Policy 논문은 arbitrary normalizable distributions를 표현하고, 고차원 액션 공간을 효과적으로 처리하며, 분포적 표현력을 유지하면서 안정적인 훈련을 수행한다는 점에서 강력한 구조적 전제를 제공합니다.
- **대규모 로봇 데이터셋**: Open_X Embodiment Robotic Learning Datasets and RT X Models 논문은 527개의 기술과 160만 개 이상의 작업이 포함된 대규모 로봇 데이터셋을 제시하며, 이는 다양한 로봇 플랫폼에서 학습할 수 있는 다양성에 대한 보장입니다.

### 다음 실험 아이디어

- **vision-language-action 모델과 diffusion policy를 결합한 실험**: vision-language-action 모델이 이미지와 언어 정보를 활용하고, diffusion policy가 액션 공간을 효과적으로 처리하는 점에서 두 모델의 결합은 새로운 상황에 대한 더 높은 수준의 일반화를 가능하게 할 것입니다.
- **PaLM E 모델과 대규모 로봇 데이터셋의 조합**: PaLM-E는 다양한 internet-scale domain에서 학습한 모델을 사용하여 vision-language-action 모델과 결합할 수 있습니다. 이로 인해, PaLM-E는 대규모 로봇 데이터셋을 활용하여 다양한 상황에 대한 적절한 로봇 행동 생성이 가능합니다.

### 출처
- Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models.pdf
- RT_1_Robotics_Transformer_for_Real_World_Control.pdf
- Diffusion_Policy_Visuomotor_Policy_Learning.pdf
- PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics.pdf
- CLIP_Learning_Transferable_Visual_Models.pdf
- RT_2_Vision_Language_Action_Models.pdf
- PaLM_E_An_Embodied_Multimodal_Language_Model.pdf

## Related Papers With Sources
- [[Pages/Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models|Open X Embodiment Robotic Learning Datasets and RT X Models]] — source: `Open_X_Embodiment_Robotic_Learning_Datasets_and_RT_X_Models.pdf`, similarity: `0.587`
- [[Pages/RT_1_Robotics_Transformer_for_Real_World_Control|RT 1 Robotics Transformer for Real World Control]] — source: `RT_1_Robotics_Transformer_for_Real_World_Control.pdf`, similarity: `0.4941`
- [[Pages/Diffusion_Policy_Visuomotor_Policy_Learning|Diffusion Policy Visuomotor Policy Learning]] — source: `Diffusion_Policy_Visuomotor_Policy_Learning.pdf`, similarity: `0.4848`
- [[Pages/PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics|PerAct Perceiver Actor for Multi Task Transformer Robotics]] — source: `PerAct_Perceiver_Actor_for_Multi_Task_Transformer_Robotics.pdf`, similarity: `0.46`
- [[Pages/CLIP_Learning_Transferable_Visual_Models|CLIP Learning Transferable Visual Models]] — source: `CLIP_Learning_Transferable_Visual_Models.pdf`, similarity: `0.4449`
- [[Pages/RT_2_Vision_Language_Action_Models|RT 2 Vision Language Action Models]] — source: `RT_2_Vision_Language_Action_Models.pdf`, similarity: `0.4256`
- [[Pages/PaLM_E_An_Embodied_Multimodal_Language_Model|PaLM E An Embodied Multimodal Language Model]] — source: `PaLM_E_An_Embodied_Multimodal_Language_Model.pdf`, similarity: `0.3428`

## Follow-up Reading Plan
- Open the linked paper pages and inspect Key Claims and Source Evidence.
- Add experiment notes below after reading.

## My Notes
- 
