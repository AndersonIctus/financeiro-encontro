from typing import Optional

from app.schemas.query_params import QueryParams

class FinalidadeFilterDto(QueryParams):
    nome: Optional[str] = None