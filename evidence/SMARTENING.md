# Smartening

## Agent가 똑똑해진 지점

- PDF를 chunk 단위로 나누고 source chunk id를 page와 claim에 연결합니다.
- LLM unavailable 상황에서도 deterministic mock fallback으로 데모 재현성을 유지합니다.
- EvalAgent가 claim별 verdict, score, critical 여부를 계산합니다.
- threshold basis points를 사용해 소수점 비교 오류 없이 publication gate를 수행합니다.
- cross-link 후보를 평가한 뒤 accepted link만 최종 wiki page에 반영합니다.
- MCP 스타일 stdio server와 natural-language CLI dry-run을 제공해 course requirement와 연결합니다.
