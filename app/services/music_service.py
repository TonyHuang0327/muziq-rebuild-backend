"""音樂搜尋服務：串接 iTunes API 並回傳整理後的歌曲資料。"""
import httpx

ITUNES_API_URL = "https://itunes.apple.com/search"


async def search_music(term: str) -> dict:
    """
    依關鍵字搜尋歌曲。
    :param term: 搜尋關鍵字
    :return: {"status": "success", "data": [Song, ...]}
    :raises ValueError: 未提供搜尋關鍵字
    :raises RuntimeError: 無法取得 iTunes API 資料
    """
    if not term or not term.strip():
        raise ValueError("Search term is required")

    async with httpx.AsyncClient() as client:
        params = {
            "term": term,
            "media": "music",
            "entity": "song",
            "limit": 10,
            "country": "TW",
        }
        response = await client.get(ITUNES_API_URL, params=params)

        if response.status_code != 200:
            raise RuntimeError("Failed to fetch music data")

        data = response.json()
        results = data.get("results", [])

        clean_data = [
            {
                "id": str(song.get("trackId")),
                "title": song.get("trackName"),
                "artist": song.get("artistName"),
                "previewUrl": song.get("previewUrl"),
            }
            for song in results
        ]
        return {"status": "success", "data": clean_data}
