FROM python:3.12-slim

WORKDIR /worker

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv

RUN uv sync --frozen

COPY app ./app
COPY worker ./worker

CMD ["uv", "run", "python", "-m", "worker.worker"]