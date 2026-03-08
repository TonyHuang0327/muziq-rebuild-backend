from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    """單筆歌曲的 API 回應結構"""
    id: str
    title: str
    artist: str
    previewUrl: str | None  # iTunes 30 秒試聽連結，可能為 None

class SongResponse(BaseModel):
    status: str
    data: List[Song]