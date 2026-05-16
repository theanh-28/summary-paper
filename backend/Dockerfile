FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD sh -c "arq app.worker.worker_settings.WorkerSettings & uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
