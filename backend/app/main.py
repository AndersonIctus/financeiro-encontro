from fastapi import FastAPI

from app.routers import lancamento_router

app = FastAPI(
    title="Financeiro Encontro",
    description="Sistema financeiro para gerenciamento do encontro",
    version="1.0.0"
)

app.include_router(lancamento_router.router)

@app.get("/health")

def health():
    return {"status":"ok"}