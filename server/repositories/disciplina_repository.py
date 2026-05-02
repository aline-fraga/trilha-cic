from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import Disciplina


class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_ativas(self) -> list[Disciplina]:
        stmt = select(Disciplina).where(Disciplina.is_active.is_(True))
        return list(self.db.scalars(stmt))
