from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class ExtratoBancario(Base):
    __tablename__ = "extratos_bancarios"

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_arquivo = Column(String(500), nullable=False)
    tamanho_bytes = Column(Integer, nullable=True)
    processado_em = Column(DateTime(timezone=True), server_default=func.now())
    