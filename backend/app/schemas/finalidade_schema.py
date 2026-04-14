from pydantic import BaseModel

class FinalidadeResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None

    class Config:
        from_attributes = True