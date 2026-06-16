from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.finalidade import Finalidade
from app.models.enums import TipoLancamento

DEFAULT_FINALIDADES = [
    # ── RECEITA ──────────────────────────────────────────────────────────────
    {"id": 1,   "nome": "OFERTA",               "tipo": TipoLancamento.RECEITA},
    {"id": 2,   "nome": "CAMPANHA",              "tipo": TipoLancamento.RECEITA},
    {"id": 3,   "nome": "INSCRIÇÃO ENCONTRISTA", "tipo": TipoLancamento.RECEITA},
    {"id": 4,   "nome": "INSCRIÇÃO ENCONTREIRO", "tipo": TipoLancamento.RECEITA},
    {"id": 5,   "nome": "OUTROS REC.",           "tipo": TipoLancamento.RECEITA},
    # ── DESPESA ──────────────────────────────────────────────────────────────
    {"id": 101, "nome": "CAMISAS",               "tipo": TipoLancamento.DESPESA},
    {"id": 102, "nome": "CERIMONIAL",            "tipo": TipoLancamento.DESPESA},
    {"id": 103, "nome": "CÍRCULOS",              "tipo": TipoLancamento.DESPESA},
    {"id": 104, "nome": "COMBUSTÍVEL",           "tipo": TipoLancamento.DESPESA},
    {"id": 105, "nome": "COMPRAS",               "tipo": TipoLancamento.DESPESA},
    {"id": 106, "nome": "CORREIOS",              "tipo": TipoLancamento.DESPESA},
    {"id": 107, "nome": "COZINHA",               "tipo": TipoLancamento.DESPESA},
    {"id": 108, "nome": "GERAL",                 "tipo": TipoLancamento.DESPESA},
    {"id": 109, "nome": "FARMÁCIA",              "tipo": TipoLancamento.DESPESA},
    {"id": 110, "nome": "LANCHONETE",            "tipo": TipoLancamento.DESPESA},
    {"id": 111, "nome": "LIVRARIA",              "tipo": TipoLancamento.DESPESA},
    {"id": 112, "nome": "SECRETARIA",            "tipo": TipoLancamento.DESPESA},
    {"id": 113, "nome": "SERVIÇOS",              "tipo": TipoLancamento.DESPESA},
    {"id": 114, "nome": "OUTROS DESP.",          "tipo": TipoLancamento.DESPESA},
]


def seed_finalidades(db: Session):
    try:
        inserted = False

        for item in DEFAULT_FINALIDADES:
            existente = (
                db.query(Finalidade)
                .filter(Finalidade.id == item["id"])
                .first()
            )

            if not existente:
                nova = Finalidade(
                    id=item["id"],
                    nome=item["nome"],
                    tipo=item["tipo"],
                    descricao=f"Finalidade padrão: {item['nome']}",
                )
                db.add(nova)
                inserted = True

        if inserted:
            db.commit()
            reset_sequence(db)
        else:
            db.rollback()

    except Exception:
        db.rollback()
        raise


def reset_sequence(db: Session):
    db.execute(text("""
        SELECT setval('finalidades_id_seq', (SELECT MAX(id) FROM finalidades));
    """))
    db.commit()
