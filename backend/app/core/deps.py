from fastapi import Depends, Header
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token
from app.database.session import get_db
from app.services.auth_service import AuthService


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise UnauthorizedException()
        
        payload = decode_token(token)
        usuario_id = int(payload.get("sub"))
        
    except (JWTError, ValueError, AttributeError):
        raise UnauthorizedException("Token inválido ou expirado")

    return AuthService.get_by_id(db, usuario_id)
