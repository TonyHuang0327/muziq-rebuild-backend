"""搜尋相關 API 路由。"""
from fastapi import APIRouter, HTTPException
import os
from model.song import SongResponse
from services.music_service import search_music

router = APIRouter(prefix=os.getenv("API_PREFIX", "/api/v1"), tags=["search"])


@router.get("/search", response_model=SongResponse)
async def search_music_endpoint(term: str):
    """依關鍵字搜尋音樂，資料來源為 iTunes API（台灣區）。"""
    try:
        result = await search_music(term)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        print(f"Error searching music: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
