from sqlalchemy.orm import Session

from app.repositories.lancamento_repository import LancamentoRepository
from app.schemas.lancamento_schema import LancamentoCreate, LancamentoUpdate
from app.models.enums import StatusLancamento


class LancamentoService:

    @staticmethod
    def create(db: Session, data: LancamentoCreate):
        payload = data.model_dump()
        payload["status"] = StatusLancamento.NAO_CONCILIADO
        return LancamentoRepository.create(db, payload)

    @staticmethod
    def update(db: Session, lancamento_id: int, data: LancamentoUpdate):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise Exception("Lançamento não encontrado")

        updated = data.model_dump(exclude_unset=True)
        return LancamentoRepository.update(db, obj, updated)

    @staticmethod
    def delete(db: Session, lancamento_id: int):
        obj = LancamentoRepository.get_by_id(db, lancamento_id)

        if not obj:
            raise Exception("Lançamento não encontrado")

        LancamentoRepository.delete(db, obj)

    @staticmethod
    def list(db: Session, filters: dict, skip: int, limit: int):
        return LancamentoRepository.list(db, filters, skip, limit)