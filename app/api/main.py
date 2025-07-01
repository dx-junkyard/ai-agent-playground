import requests
import re
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, HTTPException, Query
from typing import Dict, List, Any
import logging

# config.pyからトークンやAPIエンドポイントをインポート
from app.api.ai import AIClient
from app.api.db import DBClient
from app.api.page_analyzer import analyze_page
from app.api.chat_analyzer import analyze_chat

app = FastAPI()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ユーザー登録エンドポイント
@app.post("/api/v1/users")
async def create_user(request: Request) -> Dict[str, str]:
    try:
        data = await request.json()
    except Exception:
        data = {}
    line_user_id = data.get("line_user_id")
    repo = DBClient()
    user_id = repo.create_user(line_user_id=line_user_id)
    return {"user_id": user_id}

# LINEのWebhookエンドポイント
@app.post("/api/v1/user-message")
async def post_usermessage(request: Request) -> Dict[str, Any]:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
   
    ai_generator = AIClient()
    message = body.get("message", "")
    user_id = body.get("user_id")
    repo = DBClient()
    if user_id:
        repo.insert_message(user_id, "user", message)

    urls = re.findall(r"https?://\S+", message)
    text_without_urls = re.sub(r"https?://\S+", "", message).strip()
    for url in urls:
        title = ""
        page_text = ""
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string if soup.title else ""
            page_text = soup.get_text(separator=" ", strip=True)
        except Exception as exc:
            logger.error("Failed to fetch %s: %s", url, exc)
        analyze_page(title=title, text=page_text, url=url, source_type="web")

    user_analysis = None
    if text_without_urls:
        user_analysis = analyze_chat(text=text_without_urls)

    ai_response = ai_generator.create_response(message)
    logger.info(f"AI response: {ai_response}")
    ai_analysis = analyze_chat(text=ai_response)
    if user_id:
        repo.insert_message(user_id, "ai", ai_response)
    return {
        "user_analysis": user_analysis,
        "ai_message": ai_response,
        "ai_analysis": ai_analysis,
    }

@app.get("/api/v1/user-messages")
async def get_user_messages(user_id: str = Query(..., description="ユーザーID"), limit: int = Query(10, ge=1, le=100, description="取得件数")) -> List[Dict]:
    repo = DBClient()
    messages = repo.get_user_messages(user_id=user_id, limit=limit)
    return messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

