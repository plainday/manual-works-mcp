# manual-works-mcp

ManualWorks 문서 검색을 위한 MCP(Model Context Protocol) 서버입니다.

ManualWorks에 검색 API가 없어서, 문서 목록/내용 API를 조합하여 키워드 검색 기능을 제공합니다.

## 설치

```bash
pip install -e .
```

## 환경변수 설정

| 이름 | 설명 | 예시 |
|---|---|---|
| `MANUALWORKS_BASE_URL` | ManualWorks 서버 URL | `http://127.0.0.1:1975` |
| `MANUALWORKS_API_UUID` | API UUID | `5b969d63e97cfec7` |

## 사용법

### MCP Inspector로 테스트

```bash
mcp dev src/manual_works_mcp/server.py
```

### Claude Desktop 설정

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "manual-works": {
      "command": "manual-works-mcp",
      "env": {
        "MANUALWORKS_BASE_URL": "http://127.0.0.1:1975",
        "MANUALWORKS_API_UUID": "your-api-uuid"
      }
    }
  }
}
```

## MCP Tools

### `search_documents`

키워드로 ManualWorks 문서를 검색합니다.

- **파라미터:** `keyword` (string) - 검색할 키워드
- **동작:** 모든 문서의 장(chapter) 내용을 가져와 키워드 매칭 후 결과를 반환
- **반환:** 매칭된 문서 제목, 장 제목, URL, 매칭된 내용 snippet

## 라이선스

Apache-2.0
