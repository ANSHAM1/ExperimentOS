import json

from aio_pika.abc import AbstractChannel, AbstractIncomingMessage

from worker.agent import ExperimentAgent


class ExperimentConsumer:

    def __init__(self, channel: AbstractChannel) -> None:
        self.channel = channel
        self.agent = ExperimentAgent()

    async def start(self) -> None:
        queue = await self.channel.declare_queue(
            "experiment_queue",
            durable=True,
        )

        await queue.consume(self._handle_message)

    async def _handle_message(
        self,
        message: AbstractIncomingMessage,
    ) -> None:

        async with message.process():
            payload = json.loads(message.body)

            await self.agent.run(payload)