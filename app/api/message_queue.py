import json
import pika
from config import MQ_HOST


def _connect() -> pika.BlockingConnection:
    """Create a connection to RabbitMQ with retries."""
    params = pika.ConnectionParameters(
        host=MQ_HOST,
        connection_attempts=5,
        retry_delay=5,
    )
    return pika.BlockingConnection(params)


def publish_message(queue: str, data: dict) -> None:
    """Publish a JSON message to the specified RabbitMQ queue."""
    connection = _connect()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()
