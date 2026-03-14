from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.lancamento_schema import LancamentoCreate
from app.services.lancamento_service import LancamentoService

router = APIRouter(prefix="/lancamentos",tags=["Lançamentos"])

@router.post("/")
def criar_lancamento(
    data: LancamentoCreate,
    db: Session = Depends(get_db)
):
    service = LancamentoService(db)
    return service.criar(data)

@router.get("/")
def listar_lancamentos(
    db: Session = Depends(get_db)
):
    service = LancamentoService(db)
    return service.listar()