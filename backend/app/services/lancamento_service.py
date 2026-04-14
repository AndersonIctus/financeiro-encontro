from sqlalchemy.orm import Session

from app.repositories.lancamento_repository import LancamentoRepository
from app.schemas.lancamento_schema import LancamentoCreate, LancamentoUpdate
from app.models.enums import StatusLancamento

from app.core.exceptions import NotFoundException
from app.models.lancamento import Lancamento


class LancamentoService:

    @staticmethod
    def create(db: Session, data: LancamentoCreate):
        payload = data.model_dump()
        
        # 🔥 proteção contra duplicação
        hash_value = data.get("hash_transacao")
        if "hash" in data:
            existente = db.query(Lancamento).filter(
                Lancamento.hash_transacao == hash_value
            ).first()

            if existente:
                return existente  # ✅ evita duplicação
        
        payload["status"] = StatusLancamento.NAO_CONCILIADO
        return LancamentoRepository.create(db, payload)

    @staticmethod
    def update(db: Session, lancamento_id: int, data: LancamentoUpdate):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise NotFoundException("Lançamento")

        updated = data.model_dump(exclude_unset=True, exclude_none=True)
        return LancamentoRepository.update(db, obj, updated)

    @staticmethod
    def delete(db: Session, lancamento_id: int):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise NotFoundException("Lançamento")

        LancamentoRepository.delete(db, obj)

    @staticmethod
    def list_all(db: Session, params):
        return LancamentoRepository.list_all(db, params)

    @staticmethod
    def list(db: Session, params):
        items, total = LancamentoRepository.list_with_count(db, params)

        return {
            "items": items,
            "total": total,
            "skip": params.skip,
            "limit": params.limit
        }

    @staticmethod
    def get_by_id(db: Session, lancamento_id: int):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise NotFoundException("Lançamento")

        return obj

    @staticmethod
    def exists_by_hash(db: Session, hash_value: str) -> bool:
        return db.query(Lancamento).filter(Lancamento.hash_transacao == hash_value).first() is not None
    
    @staticmethod
    def conciliar(db, lancamento_id: int, finalidade_id: int):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise NotFoundException("Lançamento")

        obj.finalidade_id = finalidade_id
        obj.status = StatusLancamento.CONCILIADO

        db.commit()
        db.refresh(obj)

        return obj
