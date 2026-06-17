# MCP Plan

## 현재 구현

- `mcp_servers/research_vault_agent.py`는 stdio JSON-RPC 방식의 custom MCP-style server입니다.
- `tools/list`로 vault 검색, run summary, evidence lookup 같은 도구를 노출할 수 있습니다.
- `src/main.py`는 자연어 CLI dry-run과 blockchain read branch를 제공합니다.

## 다음 확장

- Filesystem MCP: vault와 evidence 파일 탐색
- Fetch MCP: 논문 URL metadata 수집
- Git MCP: 변경 이력과 submission snapshot 기록
- WorldLand read MCP: latest block, tx receipt, certificate lookup read-only 도구

현재 제출에서는 custom local MCP-style server를 데모하고, 외부 MCP 서버 실운영은 future work로 둡니다.
