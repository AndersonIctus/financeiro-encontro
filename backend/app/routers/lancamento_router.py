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
from app.schemas.pagination_schema import Page
from app.schemas.lancamento_filter_dto import LancamentoFilterDto


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


@router.get("/", response_model=Page[LancamentoResponse])
def list(
    params: LancamentoFilterDto = Depends(),
    db: Session = Depends(get_db),
):
    return LancamentoService.list(db, params)

@router.get("/all", response_model=List[LancamentoResponse])
def list_all(
    params: LancamentoFilterDto = Depends(),
    db: Session = Depends(get_db),
):
    return LancamentoService.list_all(db, params)

@router.get("/{lancamento_id}", response_model=LancamentoResponse)
def get_by_id(lancamento_id: int, db: Session = Depends(get_db)):
    return LancamentoService.get_by_id(db, lancamento_id)


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