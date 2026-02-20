# manual-works-mcp

ManualWorks 문서 검색을 위한 MCP(Model Context Protocol) 서버입니다.

ManualWorks에 검색 API가 없어서, 문서 목록/내용 API를 조합하여 키워드 검색 기능을 제공합니다.

## 설치

```bash
git clone https://github.com/plainday/manual-works-mcp.git
cd manual-works-mcp
```

### uv 사용 (권장)

```bash
uv venv
uv pip install -e .
```

### pip 사용

```bash
python -m venv .venv
```

가상환경 활성화:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

패키지 설치:

```bash
pip install -e .
```

## 환경변수 설정

| 이름 | 설명 | 예시 |
|---|---|---|
| `MANUALWORKS_BASE_URL` | ManualWorks 서버 URL | `http://127.0.0.1:1975` |
| `MANUALWORKS_API_UUID` | API UUID | `5b969d63e97cfec7` |
| `MANUALWORKS_MCP_HOST` | MCP 서버 바인딩 호스트 (선택) | `0.0.0.0` (기본값) |
| `MANUALWORKS_MCP_PORT` | MCP 서버 포트 (선택) | `8000` (기본값) |

## 사용법

### 서버 실행

#### uv 사용 (권장)

```bash
MANUALWORKS_BASE_URL=http://127.0.0.1:1975 MANUALWORKS_API_UUID=your-api-uuid uv run -m manual_works_mcp.server
```

#### pip 사용 (가상환경 활성화 후)

```bash
MANUALWORKS_BASE_URL=http://127.0.0.1:1975 MANUALWORKS_API_UUID=your-api-uuid python -m manual_works_mcp.server
```

Windows의 경우 환경변수를 먼저 설정합니다:

```cmd
set MANUALWORKS_BASE_URL=http://127.0.0.1:1975
set MANUALWORKS_API_UUID=your-api-uuid
.venv\Scripts\python.exe -m manual_works_mcp.server
```

서버가 시작되면 `http://0.0.0.0:8000/mcp` 에서 MCP 요청을 수신합니다.

### MCP Inspector로 테스트

```bash
mcp dev src/manual_works_mcp/server.py
```

### Claude Desktop 설정

Claude Desktop 메뉴에서 **File > Settings > Developer > Edit Config**를 클릭하여 설정 파일을 엽니다.

설정 파일 경로:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

서버를 먼저 실행한 후, 아래 설정을 추가합니다:

```json
{
  "mcpServers": {
    "manual-works": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

> 설정 후 Claude Desktop을 재시작합니다.

## MCP Tools

### `search_documents`

키워드로 ManualWorks 문서를 검색합니다.

- **파라미터:** `keyword` (string) - 검색할 키워드
- **동작:** 모든 문서의 장(chapter) 내용을 가져와 키워드 매칭 후 결과를 반환
- **반환:** 매칭된 문서 제목, 장 제목, URL, 매칭된 내용 snippet

## 라이선스

Apache-2.0
