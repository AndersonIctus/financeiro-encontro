import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://financeiro:financeiro@localhost:5432/financeiro_encontro"
)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")