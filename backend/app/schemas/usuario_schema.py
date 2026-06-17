from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True


class UsuarioUpdate(BaseModel):
    nome: str
    email: EmailStr
    senha: Optional[str] = None
    ativo: bool
