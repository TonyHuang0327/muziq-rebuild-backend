"""音樂搜尋服務：串接 iTunes API 並回傳整理後的歌曲資料。"""
import httpx
import logging
from fastapi import HTTPException, status

ITUNES_API_URL = "https://itunes.apple.com/search"


async def search_music(term: str) -> dict:
    """
    依關鍵字搜尋歌曲。
    :param term: 搜尋關鍵字
    :return: {"status": "success", "data": [Song, ...]}
    :raises ValueError: 未提供搜尋關鍵字
    :raises HTTPException: 無法取得 iTunes API 資料
    """
    if not term or not term.strip():
        raise HTTPException(status_code=400, detail="Search term is required")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            params = {
                "term": term,
                "media": "music",
                "entity": "song",
                "limit": 10,
                "country": "TW",
            }
            response = await client.get(ITUNES_API_URL, params=params)

            # 1. 檢查 HTTP 狀態碼 (4xx, 5xx 會拋出 HTTPStatusError)
            response.raise_for_status()
            
            # 2. 檢查 JSON 解析 (可能 iTunes 回傳了 HTML 錯誤頁面)
            data = response.json()

        except httpx.RequestError as exc:
            # 網路層級錯誤 (DNS, Connection timeout 等) -> 502
            logging.exception("Network error occurred while requesting %r", exc.request.url)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Upstream service unreachable") from exc
        except httpx.HTTPStatusError as exc:
            # iTunes 回傳了 4xx 或 5xx -> 502
            logging.exception("Error response %d while requesting %r", exc.response.status_code, exc.request.url)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Upstream service returned an error") from exc
            
        except (ValueError, KeyError) as exc:
            # JSON 解析失敗或格式不對 -> 502
            logging.exception("Data format error")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid data format from upstream") from exc

        results = data.get("results", [])

        clean_data = []
        for song in results:
            track_id = song.get("trackId")
            title = song.get("trackName")
            artist = song.get("artistName")
            
            if track_id and title and artist:
                clean_data.append({
                    "id": str(track_id),
                    "title": title,
                    "artist": artist,
                    "previewUrl": song.get("previewUrl", ""), # 給予預設空字串
                })
        
        return {"status": "success", "data": clean_data}
