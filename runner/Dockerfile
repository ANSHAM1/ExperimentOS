FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    tensorflow \
    torch \
    torchvision \
    torchaudio \
    numpy \
    pandas \
    scikit-learn

WORKDIR /runner

COPY runner ./runner

EXPOSE 9000

CMD ["uvicorn", "runner.main:app", "--host", "0.0.0.0", "--port", "9000"]