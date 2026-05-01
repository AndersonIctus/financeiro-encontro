import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://financeiro:financeiro@localhost:5432/financeiro_encontro"
)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")

JWT_SECRET = os.getenv("JWT_SECRET", "changeme-insecure-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))  # 8 horas