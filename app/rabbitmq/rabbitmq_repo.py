import json

from aio_pika import Message
from aio_pika.abc import AbstractChannel


class RabbitMQRepository:

    def __init__(self, channel: AbstractChannel) -> None:

        self.channel = channel


    async def declare_queue(self, queue_name: str, *, durable: bool = True) -> None:

        await self.channel.declare_queue(queue_name, durable=durable)


    async def publish(self, queue_name: str, payload: dict[str, object]) -> None:

        message = Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=2,
        )

        await self.channel.default_exchange.publish(message, routing_key=queue_name)