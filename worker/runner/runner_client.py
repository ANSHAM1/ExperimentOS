import httpx

from typing import Any


class RunnerClient:

    def __init__(self, base_url: str) -> None:

        self.base_url = base_url.rstrip("/")


    async def health(self) -> bool:

        async with httpx.AsyncClient() as client:

            response = await client.get(f"{self.base_url}/health", timeout=5)

            return response.is_success


    async def execute(self, *, experiment_id: str, code: str) -> dict[str, Any]:

        async with httpx.AsyncClient(timeout=310) as client:

            response = await client.post(
                f"{self.base_url}/execute",

                json={
                    "experiment_id": experiment_id,
                    "code": code,
                },
            )

            response.raise_for_status()

            return response.json()