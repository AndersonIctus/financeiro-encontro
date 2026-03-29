from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.session import SessionLocal
from app.services.lancamento_service import LancamentoService
from app.schemas.lancamento_schema import (
    LancamentoCreate,
    LancamentoUpdate,
    LancamentoResponse
)
from app.models.enums import StatusLancamento, TipoLancamento


router = APIRouter(prefix="/lancamentos", tags=["Lançamentos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=LancamentoResponse)
def create(data: LancamentoCreate, db: Session = Depends(get_db)):
    return LancamentoService.create(db, data)


@router.get("/", response_model=List[LancamentoResponse])
def list(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    status: Optional[StatusLancamento] = None,
    tipo: Optional[TipoLancamento] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    filters = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "status": status,
        "tipo": tipo,
    }

    return LancamentoService.list(db, filters, skip, limit)


@router.put("/{lancamento_id}", response_model=LancamentoResponse)
def update(
    lancamento_id: int,
    data: LancamentoUpdate,
    db: Session = Depends(get_db),
):
    return LancamentoService.update(db, lancamento_id, data)


@router.delete("/{lancamento_id}")
def delete(lancamento_id: int, db: Session = Depends(get_db)):
    LancamentoService.delete(db, lancamento_id)
    return {"message": "Lançamento removido com sucesso"}