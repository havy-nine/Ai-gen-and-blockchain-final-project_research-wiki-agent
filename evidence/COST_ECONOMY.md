# Cost And Economy

## 현재 mock economy

- 보상 단위: accepted EvalAgent finding당 `0.01 WLC` mock payment
- 최신 run accepted finding payments: `545`
- 최신 run total mock WLC: `5.45`
- 보상 대상: 통과한 page가 아니라 `curator_decision == ACCEPT`인 finding

## Reward ablation

| policy | accepted findings | payments | total mock WLC |
|---|---:|---:|---:|
| no_reward | 545 | 0 | 0.0 |
| accepted_findings | 545 | 545 | 5.45 |

## 실제 WLC가 필요한 경우

실제 WorldLand 테스트넷으로 확장하면 WLC는 contract deploy gas, `certifyPage` gas, accepted finding reward, retry buffer에만 씁니다. 현재 제출 데모에는 실제 WLC가 필요하지 않습니다.
