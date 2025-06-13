import json
import logging
import os
import pika
from dotenv import load_dotenv
from openai import OpenAI

from config import MQ_HOST, MQ_RAW_QUEUE, MQ_PROCESSED_QUEUE, ROOT_CATEGORIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
ai_model = os.getenv("AI_MODEL", "gpt-4o")

PROMPT_TEMPLATE = """
次のWebページ内容を短く日本語で要約し、root_categoriesから適切なものを選んでサブカテゴリー名を1つずつ推測してください。JSONのみ出力してください。

root_categories = {roots}

# 出力フォーマット
{{
  "summary": "...",
  "labels": [{{"root": "...", "sub": "..."}}]
}}

[入力]
タイトル:{title}
本文:{text}
"""


def analyze_action(data: dict) -> dict:
    title = data.get("title", "")
    text = data.get("text", "")[:1000]
    prompt = PROMPT_TEMPLATE.format(title=title, text=text, roots=ROOT_CATEGORIES)
    try:
        response = client.chat.completions.create(
            model=ai_model,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as exc:
        logger.error(f"OpenAI API error: {exc}")
        return {"summary": text[:200], "labels": []}


def main() -> None:
    params = pika.ConnectionParameters(
        host=MQ_HOST,
        connection_attempts=5,
        retry_delay=5,
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=MQ_RAW_QUEUE, durable=True)
    channel.queue_declare(queue=MQ_PROCESSED_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        analyzed = analyze_action(data)
        data.update(analyzed)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        publish_params = pika.ConnectionParameters(
            host=MQ_HOST,
            connection_attempts=5,
            retry_delay=5,
        )
        publish_connection = pika.BlockingConnection(publish_params)
        publish_channel = publish_connection.channel()
        publish_channel.queue_declare(queue=MQ_PROCESSED_QUEUE, durable=True)
        publish_channel.basic_publish(
            exchange="",
            routing_key=MQ_PROCESSED_QUEUE,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        publish_connection.close()
        logger.info("Processed action sent to next queue")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MQ_RAW_QUEUE, on_message_callback=callback)
    logger.info("Summarize worker started. Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
