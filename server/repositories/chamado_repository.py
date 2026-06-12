from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import Chamado
from server.models.enums import ChamadoStatus, ChamadoTipo


class ChamadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, chamado: Chamado) -> Chamado:
        self.db.add(chamado)
        self.db.commit()
        self.db.refresh(chamado)
        return chamado

    def listar(
        self, status: str | None = None, tipo: str | None = None
    ) -> list[Chamado]:
        stmt = select(Chamado)
        if status is not None:
            stmt = stmt.where(Chamado.status == status)
        if tipo is not None:
            stmt = stmt.where(Chamado.tipo == tipo)
        stmt = stmt.order_by(Chamado.created_at.desc())
        return list(self.db.scalars(stmt))

    def buscar(self, chamado_id: int) -> Chamado | None:
        stmt = select(Chamado).where(Chamado.id == chamado_id)
        return self.db.scalars(stmt).one_or_none()
