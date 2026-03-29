from fastapi import FastAPI

from app.routers.lancamento_router import router as lancamento_router

from app.database.session import SessionLocal
from app.utils.seed import run_seed

app = FastAPI(
    title="Financeiro Encontro",
    description="Sistema financeiro para gerenciamento do encontro",
    version="1.0.0"
)

app.include_router(lancamento_router)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
