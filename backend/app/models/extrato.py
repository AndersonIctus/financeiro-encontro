from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime

from app.database.base import Base

class Extrato(Base):

    __tablename__="extratos"

    id=Column(Integer,primary_key=True)
    nome_arquivo=Column(String)
    caminho=Column(String)
    data_upload=Column(DateTime,default=datetime.utcnow)