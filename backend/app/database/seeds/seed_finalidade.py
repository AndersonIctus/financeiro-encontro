from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.finalidade import Finalidade

DEFAULT_FINALIDADES = [
    {"id": 1, "nome": "OFERTA"},
    {"id": 2, "nome": "CAMPANHA"},
    {"id": 3, "nome": "INSCRICAO ENCONTRISTA"},
    {"id": 4, "nome": "INSCRICAO ENCONTREIRO"},
    {"id": 99, "nome": "OUTROS"},
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
