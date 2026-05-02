import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://db_financeiro:fin_pass@localhost:5432/financeiro_encontro"
)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

JWT_SECRET = os.getenv("JWT_SECRET", "changeme-insecure-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))

SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"