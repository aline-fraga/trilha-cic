from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models import Curriculo


class CurriculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, is_active: bool | None = None) -> list[Curriculo]:
        stmt = select(Curriculo).options(selectinload(Curriculo.disciplinas))
        if is_active is not None:
            stmt = stmt.where(Curriculo.is_active.is_(is_active))
        stmt = stmt.order_by(Curriculo.ano_vigencia.desc())
        return list(self.db.scalars(stmt))

    def obter(self, curriculo_id: int) -> Curriculo | None:
        stmt = (
            select(Curriculo)
            .where(Curriculo.id == curriculo_id)
            .options(selectinload(Curriculo.disciplinas))
        )
        return self.db.scalars(stmt).one_or_none()
