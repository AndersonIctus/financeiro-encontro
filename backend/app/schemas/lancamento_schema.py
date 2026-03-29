from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.enums import TipoLancamento, FormaPagamento, StatusLancamento


class LancamentoBase(BaseModel):
    descricao: str = Field(..., min_length=3, max_length=255)
    valor: float = Field(..., gt=0)
    tipo: TipoLancamento
    forma_pagamento: FormaPagamento
    data_pagamento: datetime
    finalidade_id: Optional[int]
    observacao: Optional[str]


class LancamentoCreate(LancamentoBase):
    pass


class LancamentoUpdate(BaseModel):
    descricao: Optional[str]
    valor: Optional[float]
    tipo: Optional[TipoLancamento]
    forma_pagamento: Optional[FormaPagamento]
    status: Optional[StatusLancamento]
    data_pagamento: Optional[datetime]
    finalidade_id: Optional[int]
    observacao: Optional[str]


class LancamentoResponse(LancamentoBase):
    id: int
    status: StatusLancamento
    criado_em: datetime

    class Config:
        from_attributes = True