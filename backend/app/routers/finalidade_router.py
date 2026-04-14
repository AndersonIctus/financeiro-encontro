from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.finalidade_service import FinalidadeService
from app.schemas.finalidade_schema import FinalidadeResponse
from app.schemas.pagination_schema import Page
from app.schemas.finalidade_filter_dto import FinalidadeFilterDto

router = APIRouter(prefix="/finalidades", tags=["Finalidades"])


@router.get("/", response_model=Page[FinalidadeResponse])
def list(
    params: FinalidadeFilterDto = Depends(),
    db: Session = Depends(get_db),
):
    return FinalidadeService.list(db, params)

@router.get("/all", response_model=List[FinalidadeResponse])
def list_all(
    params: FinalidadeFilterDto = Depends(),
    db: Session = Depends(get_db)
):
    return FinalidadeService.list_all(db, params)


@router.get("/{finalidade_id}", response_model=FinalidadeResponse)
def get_by_id(finalidade_id: int, db: Session = Depends(get_db)):
    return FinalidadeService.get_by_id(db, finalidade_id)