# Muziq Backend

音樂搜尋 API 後端服務，使用 FastAPI 串接 iTunes API，提供歌曲搜尋與預覽連結。

## 技術棧

- **Python 3**
- **FastAPI** — Web 框架
- **httpx** — 非同步 HTTP 客戶端（呼叫 iTunes API）
- **uvicorn** — ASGI 伺服器
- **Pydantic** — 資料驗證與設定

## 專案結構

```
backend/
├── app/
│   ├── main.py          # FastAPI 應用與搜尋 API
│   └── model/
│       └── song.py      # 歌曲資料模型 (Pydantic)
├── requirements.txt     # Python 依賴
├── .gitignore
└── README.md
```

## 環境需求

- Python 3.10+
- 可連線至 iTunes API（`https://itunes.apple.com`）

## 安裝與執行

### 1. 建立虛擬環境

```bash
cd backend
python -m venv venv
```

### 2. 啟動虛擬環境

- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (CMD):** `venv\Scripts\activate.bat`
- **macOS/Linux:** `source venv/bin/activate`

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

### 4. 啟動伺服器

從 `backend/app` 目錄執行（因 `main.py` 位於 `app` 下）：

```bash
cd app
uvicorn main:app --reload
```

預設為 http://127.0.0.1:8000。  
開發時使用 `--reload` 會自動重載程式碼變更。

## API 說明

### 搜尋音樂 `GET /api/v1/search`

依關鍵字搜尋歌曲，資料來源為 iTunes API（台灣區），回傳精簡欄位。

**查詢參數**

| 參數 | 類型   | 必填 | 說明       |
| ---- | ------ | ---- | ---------- |
| term | string | 是   | 搜尋關鍵字 |

**範例請求**

```http
GET /api/v1/search?term=周杰倫
```

**成功回應 (200)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "123456789",
      "title": "歌曲名稱",
      "artist": "藝人名稱",
      "previewUrl": "https://audio-ssl.itunes.apple.com/..."
    }
  ]
}
```

**錯誤回應**

- **400** — 未提供 `term`
- **502** — 無法取得 iTunes API 資料
- **500** — 伺服器內部錯誤

**說明**

- 目前每次搜尋最多回傳 **10 筆** 結果（`limit=10`），地區為 **TW**。
- `previewUrl` 為 30 秒試聽檔連結，可直接用於前端播放。

## 互動式文件

啟動服務後可至以下網址查看與測試 API：

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 環境變數

若有敏感設定或需覆寫預設值，可於專案根目錄建立 `.env`（已列入 `.gitignore`），並在程式中以 `python-dotenv` 等讀取。目前 API 無必填環境變數。

## 授權與備註

- 搜尋資料來自 [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/)。
- 本後端僅供學習與專案使用，請遵守 Apple 相關使用條款。
