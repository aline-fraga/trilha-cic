from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models import Disciplina


class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def _com_prerequisitos(self):
        return selectinload(Disciplina.prerequisitos)

    def listar_ativas(self) -> list[Disciplina]:
        stmt = (
            select(Disciplina)
            .where(Disciplina.is_active.is_(True))
            .options(self._com_prerequisitos())
        )
        return list(self.db.scalars(stmt))

    def get_by_id(self, disciplina_id: int) -> Disciplina | None:
        stmt = (
            select(Disciplina)
            .where(Disciplina.id == disciplina_id)
            .options(self._com_prerequisitos())
        )
        return self.db.scalar(stmt)

    def get_by_codigo(self, codigo: str) -> Disciplina | None:
        stmt = select(Disciplina).where(Disciplina.codigo == codigo)
        return self.db.scalar(stmt)

    def get_many_by_ids(self, ids: list[int]) -> list[Disciplina]:
        if not ids:
            return []
        stmt = select(Disciplina).where(Disciplina.id.in_(ids))
        return list(self.db.scalars(stmt))

    def criar(self, disciplina: Disciplina) -> Disciplina:
        self.db.add(disciplina)
        self.db.flush()
        self.db.refresh(disciplina)
        return disciplina

    def inativar(self, disciplina: Disciplina) -> Disciplina:
        disciplina.is_active = False
        self.db.flush()
        return disciplina
