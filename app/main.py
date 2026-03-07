from fastapi import FastAPI, HTTPException
import httpx
app = FastAPI()

ITUNES_API_URL = "https://itunes.apple.com/search"

@app.get("/api/v1/search")
async def search_music(term: str):
    if not term:
        raise HTTPException(status_code=400, detail="Search term is required")
    async with httpx.AsyncClient() as client:
        try:
            params = {
                "term": term,
                "media": "music",
                "entity": "song",
                "limit": 5, # 先限制 5 筆，維持效能
                "country": "TW"
            }
            response = await client.get(ITUNES_API_URL, params=params)

            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Failed to fetch music data")

            data = response.json()
            results = data.get("results", [])

            clean_data = [
                {
                    "id": str(song.get("trackId")),
                    "title": song.get("trackName"),
                    "artist": song.get("artistName"),
                    "previewUrl": song.get("previewUrl")
                }
                for song in results
            ]
            return {"status": "success", "data": clean_data}
        except Exception as e:
            print(f"Error searching music: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")