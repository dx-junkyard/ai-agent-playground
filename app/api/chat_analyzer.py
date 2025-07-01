import json
import logging
import os
import re
import hashlib
import mysql.connector
from dotenv import load_dotenv
from openai import OpenAI

from config import (
    ROOT_CATEGORIES,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_PORT,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
ai_model = os.getenv("AI_MODEL", "gpt-4o")

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'port': DB_PORT,
    'charset': 'utf8mb4',
}

PROMPT_TEMPLATE = """次の発言内容を読み、root_categories から該当するカテゴリを複数選び、\
それぞれの root ラベルに対応するサブカテゴリー名の配列を推測してください。\n出力は JSON のみとし、以下の形式に従ってください。\n\nroot_categories = {roots}\n\n# 出力フォーマット\n{{\n  \"labels\": [{{\"root\": \"...\", \"sub\": [\"...\"]}}]\n}}\n\n[入力]\n{text}"""


def analyze_chat(text: str) -> dict:
    """Analyze chat message and store categories in the DB."""
    text = text[:1000]
    text_hash = hashlib.sha256(text.encode()).hexdigest()

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT labels FROM pages WHERE url_hash=%s",
            (text_hash,),
        )
        row = cursor.fetchone()
        if row:
            labels = json.loads(row["labels"] or "[]")
            return {"labels": labels}
    except mysql.connector.Error as err:
        logger.error("MySQL error: %s", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    prompt = PROMPT_TEMPLATE.format(text=text, roots=ROOT_CATEGORIES)
    logger.info("Requesting chat analysis from OpenAI")
    logger.debug("Prompt: %s", prompt)
    try:
        response = client.chat.completions.create(
            model=ai_model,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = re.sub(r'^```(?:json)?\s*', '', content, flags=re.IGNORECASE)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
        result = json.loads(content)
    except Exception as exc:
        logger.error(f"OpenAI API error: {exc}")
        result = {"labels": []}

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO pages (url, url_hash, title, summary, labels, source_type)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE labels=VALUES(labels), source_type=VALUES(source_type)
            """,
            (
                "",
                text_hash,
                "",
                None,
                json.dumps(result.get("labels", []), ensure_ascii=False),
                "chat",
            ),
        )
        conn.commit()
    except mysql.connector.Error as err:
        logger.error("MySQL error: %s", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return result
