from sqlalchemy.orm import Session

from app.database.seeds.seed_finalidade import seed_finalidades

def run_seed(db: Session):
    seed_finalidades(db)