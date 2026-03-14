from app.models.lancamento import Lancamento

class LancamentoService:
    def __init__(self,db):
        self.db=db

    def criar(self,data):
        lancamento=Lancamento(**data.dict())
        self.db.add(lancamento)
        self.db.commit()
        self.db.refresh(lancamento)
        return lancamento

    def listar(self):
        return self.db.query(Lancamento).all()