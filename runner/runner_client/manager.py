import asyncio

from dataclasses import dataclass

from .executor import PythonExecutor


@dataclass(slots=True)
class ExecutionJob:

    experiment_id: str
    code: str

    future: asyncio.Future[
        tuple[int, str, str]
    ]


class ExecutionManager:

    def __init__(
        self,
        *,
        workers: int = 2,
        timeout: int = 300,
    ) -> None:

        self.workers = workers

        self.queue: asyncio.Queue[
            ExecutionJob
        ] = asyncio.Queue()

        self.executor = PythonExecutor(
            timeout=timeout,
        )

        self._worker_tasks: list[
            asyncio.Task[None]
        ] = []

    async def start(self) -> None:

        self._worker_tasks = [
            asyncio.create_task(
                self._worker(),
                name=f"execution-worker-{index}",
            )
            for index in range(self.workers)
        ]

    async def stop(self) -> None:

        for task in self._worker_tasks:
            task.cancel()

        await asyncio.gather(
            *self._worker_tasks,
            return_exceptions=True,
        )

        self._worker_tasks.clear()

    async def submit(
        self,
        experiment_id: str,
        code: str,
    ) -> tuple[int, str, str]:

        loop = asyncio.get_running_loop()

        future: asyncio.Future[
            tuple[int, str, str]
        ] = loop.create_future()

        job = ExecutionJob(
            experiment_id=experiment_id,
            code=code,
            future=future,
        )

        await self.queue.put(job)

        return await future

    async def _worker(self) -> None:

        while True:

            job = await self.queue.get()

            try:

                result = await self.executor.execute(
                    experiment_id=job.experiment_id,
                    code=job.code,
                )

                if not job.future.done():
                    job.future.set_result(result)

            except Exception as exc:

                if not job.future.done():
                    job.future.set_exception(exc)

            finally:

                self.queue.task_done()