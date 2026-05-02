from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.core.deps import get_current_user

from app.database.seeds.main_seeds import run_seed
from app.database.session import SessionLocal

from app.routers.auth_router import router as auth_router
from app.routers.conciliacao_router import router as conciliacao_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.extrato_bancario_router import router as extrato_bancario_router
from app.routers.finalidade_router import router as finalidade_router
from app.routers.lancamento_router import router as lancamento_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Financeiro Encontro",
    description="Sistema financeiro para gerenciamento do encontro",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas públicas
app.include_router(auth_router)

# rotas protegidas
_protected = {"dependencies": [Depends(get_current_user)]}
app.include_router(lancamento_router, **_protected)
app.include_router(finalidade_router, **_protected)
app.include_router(extrato_bancario_router, **_protected)
app.include_router(conciliacao_router, **_protected)
app.include_router(dashboard_router, **_protected)


@app.get("/health")
def health():
    return {"status": "ok"}
