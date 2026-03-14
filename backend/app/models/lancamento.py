from sqlalchemy import Column,Integer,String,Numeric,DateTime,ForeignKey
from datetime import datetime

from app.database.base import Base

class Lancamento(Base):

    __tablename__ = "lancamentos"

    id = Column(Integer,primary_key=True)
    descricao = Column(String)
    nome_pagador = Column(String)
    valor = Column(Numeric)
    tipo = Column(String)
    forma_pagamento = Column(String)
    estado = Column(String)
    data_lancamento = Column(DateTime)
    finalidade_id = Column(Integer,ForeignKey("finalidades.id"))
    created_at = Column(DateTime,default=datetime.utcnow)