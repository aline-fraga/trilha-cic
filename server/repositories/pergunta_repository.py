from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import Pergunta


class PerguntaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_ativas(self) -> list[Pergunta]:
        stmt = (
            select(Pergunta)
            .where(Pergunta.is_active.is_(True))
            .order_by(Pergunta.ordem.asc(), Pergunta.id.asc())
        )
        return list(self.db.scalars(stmt))

    def listar(self, is_active: bool | None = None) -> list[Pergunta]:
        stmt = select(Pergunta)
        if is_active is not None:
            stmt = stmt.where(Pergunta.is_active.is_(is_active))
        stmt = stmt.order_by(Pergunta.ordem.asc(), Pergunta.id.asc())
        return list(self.db.scalars(stmt))

    def obter(self, pergunta_id: int) -> Pergunta | None:
        stmt = select(Pergunta).where(Pergunta.id == pergunta_id)
        return self.db.scalars(stmt).one_or_none()

    def criar(self, pergunta: Pergunta) -> Pergunta:
        self.db.add(pergunta)
        self.db.commit()
        self.db.refresh(pergunta)
        return pergunta

    def atualizar(self, pergunta: Pergunta, **campos) -> Pergunta:
        for campo, valor in campos.items():
            if valor is not None:
                setattr(pergunta, campo, valor)
        self.db.commit()
        self.db.refresh(pergunta)
        return pergunta

    def inativar(self, pergunta: Pergunta) -> Pergunta:
        pergunta.is_active = False
        self.db.commit()
        self.db.refresh(pergunta)
        return pergunta
