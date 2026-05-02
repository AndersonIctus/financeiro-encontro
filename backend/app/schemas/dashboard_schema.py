from pydantic import BaseModel
from typing import List


class TotaisResponse(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo: float
    quantidade: int


class PorDiaItem(BaseModel):
    dia: str
    total_receitas: float
    total_despesas: float
    saldo: float


class PorMesItem(BaseModel):
    mes: str
    total_receitas: float
    total_despesas: float
    saldo: float
