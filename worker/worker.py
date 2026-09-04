import asyncio

from app.core import rabbitmq
from worker.consumer import ExperimentConsumer



async def worker() -> None:

    await rabbitmq.connect()

    consumer = ExperimentConsumer(rabbitmq.channel)

    await consumer.start()

    try:
        await asyncio.Future()
    finally:
        await rabbitmq.close()



if __name__ == "__main__":
    asyncio.run(worker())