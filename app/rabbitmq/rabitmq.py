from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractChannel



class RabbitMQClient:

    def __init__(self, url: str) -> None:

        self.url = url

        self.connection: AbstractRobustConnection | None = None

        self.channel: AbstractChannel


    async def connect(self) -> None:

        self.connection = await connect_robust(self.url)

        self.channel = await self.connection.channel()

        await self.channel.set_qos(prefetch_count=1)


    async def close(self) -> None:
        
        if self.connection is not None:
            await self.connection.close()