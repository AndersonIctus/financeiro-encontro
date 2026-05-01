from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario

DEFAULT_USUARIOS = [
    {
        "nome": "Administrador",
        "email": "admin@encontro.com",
        "senha": "admin123",
    },
    {
        "nome": "Anderson Dourado",
        "email": "anderson.ictus@gmail.com",
        "senha": "andyneo84",
    },
]


def seed_usuarios(db: Session):
    try:
        inserido = False

        for item in DEFAULT_USUARIOS:
            existente = db.query(Usuario).filter(Usuario.email == item["email"]).first()
            if existente:
                continue

            db.add(Usuario(
                nome=item["nome"],
                email=item["email"],
                senha_hash=hash_password(item["senha"]),
                ativo=True,
            ))
            inserido = True

        if inserido:
            db.commit()

    except Exception:
        db.rollback()
        raise
