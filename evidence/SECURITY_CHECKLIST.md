# Security Checklist

- [x] Private key를 출력하지 않음
- [x] `.env`에 실제 secret을 넣지 않음
- [x] real payment는 demo path에서 차단
- [x] FAIL page는 `SKIP_CHAIN`으로 local-only 처리
- [x] mock tx와 real tx를 명확히 구분
- [x] certificate contract는 reject event 없이 certificate-only 설계
- [x] source-groundedness score와 critical claim gate를 함께 적용
- [x] 제출 문서에서 실제 WorldLand tx가 없다고 명시
