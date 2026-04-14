from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.finalidade import Finalidade
from app.utils.sort_utils import apply_sort

SORT_FIELDS = {
    "nome": Finalidade.nome
}

DEFAULT_SORT = "id:asc"

class FinalidadeRepository:

    @staticmethod
    def get_by_id(db: Session, finalidade_id: int):
        return db.query(Finalidade).filter(Finalidade.id == finalidade_id).first()

    @staticmethod
    def list_all(db: Session, params):
        query = db.query(Finalidade)

        if params.nome:
            query = query.filter(func.lower(Finalidade.nome).startswith(params.nome.lower()))

        query = apply_sort(query, Finalidade, params.sort, SORT_FIELDS, DEFAULT_SORT)
        
        return query.offset(params.skip).limit(params.limit).all()

    @staticmethod
    def list_with_count(db: Session, params):
        query = db.query(Finalidade)

        if params.nome:
            query = query.filter(func.lower(Finalidade.nome).startswith(params.nome.lower()))

        query = apply_sort(query, Finalidade, params.sort, SORT_FIELDS, DEFAULT_SORT)

        total = query.count()
        items = query.offset(params.skip).limit(params.limit).all()

        return items, total
    
    # 🔒 Métodos internos (sem exposição via API)
    @staticmethod
    def create(db: Session, data: dict):
        obj = Finalidade(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def update(db: Session, obj: Finalidade, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, obj: Finalidade):
        db.delete(obj)
        db.commit()