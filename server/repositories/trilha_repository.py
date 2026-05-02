from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models import Trilha, trilha_disciplinas


class TrilhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_ativas(self) -> list[Trilha]:
        stmt = (
            select(Trilha)
            .where(Trilha.is_active.is_(True))
            .options(selectinload(Trilha.disciplinas))
        )
        return list(self.db.scalars(stmt))

    def listar_por_disciplinas_ids(self, ids: list[int]) -> list[Trilha]:
        if not ids:
            return []
        stmt = (
            select(Trilha)
            .join(trilha_disciplinas, trilha_disciplinas.c.trilha_id == Trilha.id)
            .where(
                Trilha.is_active.is_(True),
                trilha_disciplinas.c.disciplina_id.in_(ids),
            )
            .distinct()
            .options(selectinload(Trilha.disciplinas))
        )
        return list(self.db.scalars(stmt))
