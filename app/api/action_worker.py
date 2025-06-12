import json
import logging
import pika

from app.api.browsing_recorder import BrowsingRecorder
from config import MQ_HOST, MQ_PROCESSED_QUEUE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    recorder = BrowsingRecorder()
    params = pika.ConnectionParameters(
        host=MQ_HOST,
        connection_attempts=5,
        retry_delay=5,
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=MQ_PROCESSED_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        recorder.insert_action(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MQ_PROCESSED_QUEUE, on_message_callback=callback)
    logger.info("DB worker started. Waiting for processed messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
