# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**manual-works-mcp**는 ManualWorks 문서 검색을 위한 MCP(Model Context Protocol) 서버입니다.
ManualWorks에 검색 API가 없어서, 문서 목록/내용 API를 조합하여 키워드 검색 기능을 제공합니다.
Apache 2.0 라이선스.

## Technology Stack

- **Language:** Python 3.10+
- **Protocol:** MCP (Model Context Protocol)
- **MCP SDK:** `mcp[cli]` (FastMCP)
- **HTTP Client:** `httpx` (async)
- **Transport:** streamable-http (기본 `127.0.0.1:8000`)
- **Build:** `hatchling`
- **Package Manager:** `uv` (권장) 또는 `pip`

## Project Structure

```
src/manual_works_mcp/
├── __init__.py
├── server.py          # MCP 서버 진입점, search_documents tool 등록
└── api_client.py      # ManualWorks REST API 클라이언트 (async httpx)
```

## Key Components

### api_client.py — `ManualWorksClient`

ManualWorks REST API 호출 클래스. URL 패턴: `{base_url}/r/api/{api_uuid}?action={action}&...`

- `get_documents()` → `DOC_LIST` (응답: `documents`)
- `get_document(doc_id)` → `DOC_GET` (파라미터: `docId`, 응답: `document`)
- `get_chapter_content(chapter_id)` → `DOC_CHAPTER_CONTENT` (파라미터: `chapterId`, 응답: `elements`)
- `get_chapter_headings(chapter_id)` → `DOC_CHAPTER_HEADING` (파라미터: `chapterId`, 응답: `headings`)

### server.py — MCP Server

`search_documents(keyword: str)` tool 1개 등록.

검색 흐름:
1. `DOC_LIST`로 전체 문서 목록 조회
2. 각 문서에 대해 `DOC_GET`으로 장(chapter) 목록 조회
3. PART > CHAPTER 재귀 구조 처리 (`_collect_chapters`)
4. 각 장에 대해 `DOC_CHAPTER_CONTENT`로 내용 조회
5. 문서 제목, 장 제목, 내용(content)에서 키워드 매칭 (대소문자 무시)
6. 매칭 결과에 문서 링크, 장 링크, 요소 링크 포함하여 반환

## Environment Variables

| 변수 | 설명 |
|---|---|
| `MANUALWORKS_BASE_URL` | ManualWorks 서버 URL (예: `http://127.0.0.1:1975`) |
| `MANUALWORKS_API_UUID` | API UUID (예: `5b969d63e97cfec7`) |
| `MANUALWORKS_MCP_HOST` | MCP 서버 바인딩 호스트 (기본: `127.0.0.1`) |
| `MANUALWORKS_MCP_PORT` | MCP 서버 포트 (기본: `8000`) |

## Development Commands

```bash
# 설치
uv venv && uv pip install -e .

# 서버 import 검증
.venv/Scripts/python.exe -c "from manual_works_mcp.server import mcp; print(mcp._tool_manager._tools.keys())"

# MCP Inspector 테스트 (Node.js 필요)
mcp dev src/manual_works_mcp/server.py
```

## API Documentation

- `api_docs/` 디렉토리에 ManualWorks 6.0 API PDF 문서 있음
- 검색 전용 API는 존재하지 않음 — 문서 순회 + 키워드 매칭 방식 사용
