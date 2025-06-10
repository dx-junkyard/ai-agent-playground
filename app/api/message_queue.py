import json
import pika
from config import MQ_HOST, MQ_QUEUE


def publish_message(data: dict) -> None:
    """Publish a JSON message to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=MQ_QUEUE, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=MQ_QUEUE,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()
