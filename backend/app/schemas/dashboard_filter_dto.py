from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import Query

from app.models.enums import FormaPagamento, StatusLancamento, TipoLancamento


class DashboardFilterDto:
    def __init__(
        self,
        data_inicio: Optional[datetime] = Query(None, description="Data inicial do período"),
        data_fim: Optional[datetime] = Query(None, description="Data final do período (default: data_inicio + 30 dias)"),
        forma_pagamento: Optional[List[FormaPagamento]] = Query(None, description="Uma ou mais formas de pagamento"),
        finalidade_id: Optional[List[int]] = Query(None, description="Um ou mais IDs de finalidade"),
        tipo: Optional[TipoLancamento] = Query(None, description="RECEITA ou DESPESA"),
        status: Optional[StatusLancamento] = Query(None, description="CONCILIADO ou NAO_CONCILIADO"),
    ):
        hoje = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        self.data_inicio = data_inicio or hoje
        self.data_fim = data_fim or (self.data_inicio + timedelta(days=30)).replace(hour=23, minute=59, second=59)
        self.forma_pagamento = forma_pagamento
        self.finalidade_id = finalidade_id
        self.tipo = tipo
        self.status = status
