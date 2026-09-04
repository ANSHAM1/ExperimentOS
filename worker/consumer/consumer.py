import json

from aio_pika.abc import AbstractIncomingMessage, AbstractChannel

from app.rabbitmq import RabbitMQRepository
from worker.dispatch import AgentDispatch

from app.core import get_settings
settings = get_settings()



class ExperimentConsumer:

    def __init__(self, channel: AbstractChannel) -> None:

        self.channel = channel

    async def start(self) -> None:

        queue = await RabbitMQRepository(self.channel).declare_queue(settings.EXPERIMENT_QUEUE, durable=True)

        await queue.consume(self._handle_message)


    async def _handle_message(self, message: AbstractIncomingMessage) -> None:

        async with message.process():
            payload = json.loads(message.body)

            await AgentDispatch.run(payload)