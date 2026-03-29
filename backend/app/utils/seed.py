from sqlalchemy.orm import Session

from app.models.finalidade import Finalidade


DEFAULT_FINALIDADES = [
    "OFERTA",
    "CAMPANHA",
    "INSCRICAO_ENCONTRISTA",
    "INSCRICAO_ENCONTREIRO",
]


def seed_finalidades(db: Session):
    for nome in DEFAULT_FINALIDADES:
        existente = (
            db.query(Finalidade)
            .filter(Finalidade.nome == nome)
            .first()
        )

        if not existente:
            nova = Finalidade(
                nome=nome,
                descricao=f"Finalidade padrão: {nome}"
            )
            db.add(nova)

    db.commit()
    
def run_seed(db: Session):
    seed_finalidades(db)