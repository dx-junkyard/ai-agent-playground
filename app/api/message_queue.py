import json
import pika
from config import MQ_HOST


def publish_message(queue: str, data: dict) -> None:
    """Publish a JSON message to the specified RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()
