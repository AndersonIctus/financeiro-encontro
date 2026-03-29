from sqlalchemy.orm import Session
from app.models.lancamento import Lancamento


class LancamentoRepository:

    @staticmethod
    def create(db: Session, data: dict) -> Lancamento:
        obj = Lancamento(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, lancamento_id: int):
        return db.query(Lancamento).filter(Lancamento.id == lancamento_id).first()

    @staticmethod
    def delete(db: Session, obj: Lancamento):
        db.delete(obj)
        db.commit()

    @staticmethod
    def update(db: Session, obj: Lancamento, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def list(db: Session, filters: dict, skip: int, limit: int):
        query = db.query(Lancamento)

        if filters.get("data_inicio"):
            query = query.filter(Lancamento.data_pagamento >= filters["data_inicio"])

        if filters.get("data_fim"):
            query = query.filter(Lancamento.data_pagamento <= filters["data_fim"])

        if filters.get("status"):
            query = query.filter(Lancamento.status == filters["status"])

        if filters.get("tipo"):
            query = query.filter(Lancamento.tipo == filters["tipo"])

        return query.offset(skip).limit(limit).all()