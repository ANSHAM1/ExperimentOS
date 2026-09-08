from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from runner.runner_client import ExecutionManager
from runner.models import  ExecuteRequest, ExecuteResponse


execution_manager = ExecutionManager(
    workers=2,
    timeout=300,
)


@asynccontextmanager
async def lifespan(_: FastAPI):

    await execution_manager.start()

    yield

    await execution_manager.stop()


app = FastAPI(
    title="ExperimentOS Runner",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, object]:

    return {
        "status": "ok",
        "queue_size": execution_manager.queue.qsize(),
        "workers": execution_manager.workers,
    }


@app.post(
    "/execute",
    response_model=ExecuteResponse,
)
async def execute(
    request: ExecuteRequest,
) -> ExecuteResponse:

    try:

        (
            exit_code,
            stdout,
            stderr,
        ) = await execution_manager.submit(
            experiment_id=request.experiment_id,
            code=request.code,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Execution failed.",
        ) from exc

    return ExecuteResponse(
        experiment_id=request.experiment_id,
        success=exit_code == 0,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
    )