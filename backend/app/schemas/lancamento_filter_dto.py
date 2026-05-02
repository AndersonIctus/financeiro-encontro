from datetime import datetime
from typing import Optional

from app.models.enums import StatusLancamento, TipoLancamento
from app.schemas.query_params import QueryParams


class LancamentoFilterDto(QueryParams):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    status: Optional[StatusLancamento] = None
    tipo: Optional[TipoLancamento] = None
    finalidade_id: Optional[int] = None