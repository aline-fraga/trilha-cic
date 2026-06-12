from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models import Disciplina, SugestaoTrilha


class SugestaoTrilhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, aluno_id: int | None = None) -> list[SugestaoTrilha]:
        stmt = (
            select(SugestaoTrilha)
            .options(selectinload(SugestaoTrilha.disciplinas))
            .order_by(SugestaoTrilha.created_at.desc())
        )
        if aluno_id is not None:
            stmt = stmt.where(SugestaoTrilha.aluno_id == aluno_id)
        return list(self.db.scalars(stmt))

    def obter(self, sugestao_id: int) -> SugestaoTrilha | None:
        stmt = (
            select(SugestaoTrilha)
            .where(SugestaoTrilha.id == sugestao_id)
            .options(selectinload(SugestaoTrilha.disciplinas))
        )
        return self.db.scalars(stmt).one_or_none()

    def criar(
        self,
        aluno_id: int,
        chamado_id: int,
        nome_proposto: str,
        disciplinas: list[Disciplina],
    ) -> SugestaoTrilha:
        sugestao = SugestaoTrilha(
            aluno_id=aluno_id,
            chamado_id=chamado_id,
            nome_proposto=nome_proposto,
            disciplinas=disciplinas,
        )
        self.db.add(sugestao)
        self.db.commit()
        self.db.refresh(sugestao)
        return sugestao
