import json
import logging
import pika

from app.api.browsing_recorder import BrowsingRecorder
from config import MQ_HOST, MQ_QUEUE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_action(data: dict) -> dict:
    """Placeholder for action analysis."""
    return data


def main() -> None:
    recorder = BrowsingRecorder()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=MQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        analyzed = analyze_action(data)
        recorder.insert_action(analyzed)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MQ_QUEUE, on_message_callback=callback)
    logger.info("Worker started. Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
