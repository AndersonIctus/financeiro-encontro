from fastapi import FastAPI

from app.routers.lancamento_router import router as lancamento_router
from app.routers.finalidade_router import router as finalidade_router
from app.routers.extrato_bancario_router import router as extrato_bancario_router

from app.database.session import SessionLocal
from app.database.seeds.main_seeds import run_seed

app = FastAPI(
    title="Financeiro Encontro",
    description="Sistema financeiro para gerenciamento do encontro",
    version="1.0.0"
)

app.include_router(lancamento_router)
app.include_router(finalidade_router)
app.include_router(extrato_bancario_router)

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
