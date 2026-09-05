FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install \
    tensorflow \
    torch \
    torchvision \
    torchaudio \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    seaborn

WORKDIR /runner

COPY runner.py /runner/runner.py

CMD ["python", "/runner/runner.py"]