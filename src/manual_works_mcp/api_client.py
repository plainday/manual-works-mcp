import httpx


class ManualWorksClient:
    def __init__(self, base_url: str, api_uuid: str):
        self.base_url = base_url.rstrip("/")
        self.api_uuid = api_uuid
        self._client = httpx.AsyncClient(timeout=30.0)

    def _build_url(self, action: str, **params: str) -> str:
        url = f"{self.base_url}/r/api/{self.api_uuid}?action={action}"
        for key, value in params.items():
            url += f"&{key}={value}"
        return url

    async def get_documents(self) -> list[dict]:
        """DOC_LIST: 전체 문서 목록 조회"""
        url = self._build_url("DOC_LIST")
        resp = await self._client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("documents", [])

    async def get_document(self, doc_id: str) -> dict:
        """DOC_GET: 문서 상세 조회 (장 목록 포함)"""
        url = self._build_url("DOC_GET", docId=doc_id)
        resp = await self._client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("document", {})

    async def get_chapter_content(self, chapter_id: str) -> list[dict]:
        """DOC_CHAPTER_CONTENT: 장 내용 조회"""
        url = self._build_url("DOC_CHAPTER_CONTENT", chapterId=chapter_id)
        resp = await self._client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("elements", [])

    async def get_chapter_headings(self, chapter_id: str) -> list[dict]:
        """DOC_CHAPTER_HEADING: 장 제목 목록 조회"""
        url = self._build_url("DOC_CHAPTER_HEADING", chapterId=chapter_id)
        resp = await self._client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("headings", [])

    async def close(self):
        await self._client.aclose()
