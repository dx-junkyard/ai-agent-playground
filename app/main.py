import requests
from fastapi import FastAPI, Request, HTTPException
from typing import Dict
import logging

# config.pyからトークンやAPIエンドポイントをインポート
from app.interest_response_generator import InterestResponseGenerator

app = FastAPI()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINEのWebhookエンドポイント
@app.post("/api/v1/user-message")
async def post_usermessage(request: Request) -> str:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
   
    #repo = CuriosityLogRepository()
    generator = InterestResponseGenerator()
    message = body.get("message", "")
    ai_response = generator.create_response(message)
    logger.info(f"AI response: {ai_response}")
    return ai_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

