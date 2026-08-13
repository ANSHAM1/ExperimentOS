from fastapi import FastAPI

from app.routes import auth_router


app = FastAPI(
    title="ExperimentOS",
    version="0.1.0",
)


app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok"}