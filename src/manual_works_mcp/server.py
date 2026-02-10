import os

from mcp.server.fastmcp import FastMCP

from manual_works_mcp.api_client import ManualWorksClient

mcp = FastMCP("ManualWorks")


def _get_client() -> ManualWorksClient:
    base_url = os.environ.get("MANUALWORKS_BASE_URL", "")
    api_uuid = os.environ.get("MANUALWORKS_API_UUID", "")
    if not base_url or not api_uuid:
        raise ValueError(
            "MANUALWORKS_BASE_URL and MANUALWORKS_API_UUID environment variables must be set"
        )
    return ManualWorksClient(base_url, api_uuid)


def _extract_text_and_urls(elements: list[dict]) -> list[dict]:
    """요소 목록에서 텍스트와 URL을 추출한다."""
    results = []
    for elem in elements:
        content = elem.get("content", "")
        url = elem.get("url", "")
        if content:
            results.append({"content": content, "url": url})
    return results


def _collect_chapters(doc: dict) -> list[dict]:
    """문서에서 모든 장(chapter)을 재귀적으로 수집한다. PART > CHAPTER 구조 처리."""
    chapters = []
    for ch in doc.get("chapters", []):
        ch_type = ch.get("type", "")
        if ch_type == "PART":
            for sub_ch in ch.get("chapters", []):
                chapters.append(sub_ch)
        else:
            chapters.append(ch)
    return chapters


@mcp.tool()
async def search_documents(keyword: str) -> str:
    """ManualWorks 문서에서 키워드로 검색합니다.

    문서 제목, 장 제목, 장 내용에서 키워드를 검색하여 매칭된 결과를 반환합니다.
    각 결과에는 해당 문서/장으로 바로 이동할 수 있는 링크가 포함됩니다.

    Args:
        keyword: 검색할 키워드
    """
    client = _get_client()
    try:
        keyword_lower = keyword.lower()
        results: list[str] = []

        documents = await client.get_documents()

        for doc_summary in documents:
            doc_id = doc_summary.get("id", "")
            doc_title = doc_summary.get("title", "")
            doc_url = doc_summary.get("url", "")

            doc = await client.get_document(doc_id)
            chapters = _collect_chapters(doc)

            for ch in chapters:
                chapter_id = ch.get("id", "")
                chapter_title = ch.get("title", "")
                chapter_url = ch.get("url", "")

                # 장 내용 조회
                elements = await client.get_chapter_content(chapter_id)
                content_items = _extract_text_and_urls(elements)
                full_text = " ".join(item["content"] for item in content_items)

                # 키워드 매칭 (대소문자 무시)
                title_match = keyword_lower in doc_title.lower()
                chapter_title_match = keyword_lower in chapter_title.lower()
                content_match = keyword_lower in full_text.lower()

                if title_match or chapter_title_match or content_match:
                    entry = f"## 문서: {doc_title}\n"
                    if doc_url:
                        entry += f"문서 링크: {doc_url}\n"
                    entry += "\n"
                    entry += f"### 장: {chapter_title}\n"
                    if chapter_url:
                        entry += f"장 링크: {chapter_url}\n"
                    entry += "\n"

                    if content_match:
                        # 매칭된 요소에서 snippet과 URL 추출
                        matched_items = _find_matched_elements(
                            content_items, keyword_lower
                        )
                        if matched_items:
                            entry += "매칭된 내용:\n"
                            for item in matched_items:
                                snippet = _make_snippet(
                                    item["content"], keyword_lower
                                )
                                if item["url"]:
                                    entry += f"- {snippet}\n  링크: {item['url']}\n"
                                else:
                                    entry += f"- {snippet}\n"
                    elif title_match:
                        entry += "매칭: 문서 제목에서 키워드 발견\n"
                    elif chapter_title_match:
                        entry += "매칭: 장 제목에서 키워드 발견\n"

                    results.append(entry)

        if not results:
            return f"'{keyword}'에 대한 검색 결과가 없습니다."

        header = f"'{keyword}' 검색 결과 ({len(results)}건):\n\n"
        return header + "\n---\n\n".join(results)
    finally:
        await client.close()


def _find_matched_elements(
    content_items: list[dict], keyword_lower: str, max_items: int = 5
) -> list[dict]:
    """키워드가 포함된 요소들을 찾는다."""
    matched = []
    for item in content_items:
        if keyword_lower in item["content"].lower():
            matched.append(item)
            if len(matched) >= max_items:
                break
    return matched


def _make_snippet(text: str, keyword_lower: str, context_chars: int = 80) -> str:
    """텍스트에서 키워드 주변 snippet을 생성한다."""
    idx = text.lower().find(keyword_lower)
    if idx == -1:
        return text[:200] + ("..." if len(text) > 200 else "")

    snippet_start = max(0, idx - context_chars)
    snippet_end = min(len(text), idx + len(keyword_lower) + context_chars)

    snippet = text[snippet_start:snippet_end].strip()
    if snippet_start > 0:
        snippet = "..." + snippet
    if snippet_end < len(text):
        snippet = snippet + "..."

    return snippet


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
