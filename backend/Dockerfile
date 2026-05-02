FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_PORT=8000
ENV DATABASE_URL=postgresql://financeiro:financeiro@localhost:5432/financeiro_encontro
ENV UPLOAD_FOLDER=/app/uploads

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}
