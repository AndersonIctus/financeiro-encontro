from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class LancamentoCreate(BaseModel):

    descricao:str
    nome_pagador:str
    valor:Decimal
    tipo:str
    forma_pagamento:str
    finalidade_id:int
    data_lancamento:datetime