FROM python:3.12-slim

# Copy uv from the official uv image.
# Pin this version in your real production build.
COPY --from=ghcr.io/astral-sh/uv:0.12.9 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /experiment

RUN uv pip install --system \
    numpy \
    pandas \
    scikit-learn \
    tensorflow \
    datasets \
    transformers

RUN useradd \
    --create-home \
    --uid 10001 \
    --shell /usr/sbin/nologin \
    runner

RUN chown -R runner:runner /experiment

USER runner

ENTRYPOINT ["python", "/experiment/main.py"]