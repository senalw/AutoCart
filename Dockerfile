FROM python:3.11.9-slim-bookworm AS builder

WORKDIR /AutoCart

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11.9-slim-bookworm
LABEL author='SenalW'

ENV PYTHONUNBUFFERED=1

WORKDIR /AutoCart

COPY --from=builder /install /usr/local
COPY settings.py .
COPY src ./src/
COPY resources ./resources/

RUN useradd --system --create-home appuser
USER appuser

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health', timeout=3)"]

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8010"]
