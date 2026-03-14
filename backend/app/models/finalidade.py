from sqlalchemy import Column,Integer,String
from app.database.base import Base

class Finalidade(Base):

    __tablename__ = "finalidades"

    id = Column(Integer,primary_key=True)
    nome = Column(String,nullable=False)
    descricao = Column(String)