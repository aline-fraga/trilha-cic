from datetime import datetime

from sqlalchemy import func, select, union_all
from sqlalchemy.orm import Session, selectinload

from server.models import Trilha, solicitacao_trilhas_candidatas
from server.models.enums import SolicitacaoStatus
from server.models.solicitacao import Solicitacao


class SolicitacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def agregar_por_trilha(
        self, periodo_inicio: datetime, periodo_fim: datetime
    ) -> list[tuple[int, SolicitacaoStatus, int]]:
        aceites_stmt = (
            select(
                Solicitacao.trilha_aceita_id.label("trilha_id"),
                Solicitacao.status.label("status"),
                func.count(Solicitacao.id).label("total"),
            )
            .where(
                Solicitacao.resolvido_em.is_not(None),
                Solicitacao.resolvido_em >= periodo_inicio,
                Solicitacao.resolvido_em <= periodo_fim,
                Solicitacao.status == SolicitacaoStatus.ACEITA,
                Solicitacao.trilha_aceita_id.is_not(None),
            )
            .group_by(Solicitacao.trilha_aceita_id, Solicitacao.status)
        )
        rejeicoes_stmt = (
            select(
                solicitacao_trilhas_candidatas.c.trilha_id.label("trilha_id"),
                Solicitacao.status.label("status"),
                func.count(Solicitacao.id).label("total"),
            )
            .join(
                Solicitacao,
                Solicitacao.id == solicitacao_trilhas_candidatas.c.solicitacao_id,
            )
            .where(
                Solicitacao.resolvido_em.is_not(None),
                Solicitacao.resolvido_em >= periodo_inicio,
                Solicitacao.resolvido_em <= periodo_fim,
                Solicitacao.status == SolicitacaoStatus.REJEITADA,
            )
            .group_by(
                solicitacao_trilhas_candidatas.c.trilha_id, Solicitacao.status
            )
        )
        return list(self.db.execute(union_all(aceites_stmt, rejeicoes_stmt)).all())

    def obter(self, solicitacao_id: int) -> Solicitacao | None:
        stmt = (
            select(Solicitacao)
            .where(Solicitacao.id == solicitacao_id)
            .options(
                selectinload(Solicitacao.trilha_aceita).selectinload(
                    Trilha.disciplinas
                ),
                selectinload(Solicitacao.trilhas_candidatas).selectinload(
                    Trilha.disciplinas
                ),
            )
        )
        return self.db.scalars(stmt).one_or_none()

    def listar(
        self,
        aluno_id: int | None = None,
        status: SolicitacaoStatus | None = None,
    ) -> list[Solicitacao]:
        stmt = select(Solicitacao).options(
            selectinload(Solicitacao.trilha_aceita).selectinload(
                Trilha.disciplinas
            ),
            selectinload(Solicitacao.trilhas_candidatas).selectinload(
                Trilha.disciplinas
            ),
        )
        if aluno_id is not None:
            stmt = stmt.where(Solicitacao.aluno_id == aluno_id)
        if status is not None:
            stmt = stmt.where(Solicitacao.status == status)
        stmt = stmt.order_by(Solicitacao.created_at.desc())
        return list(self.db.scalars(stmt))

    def existe_aceita_para_aluno(self, aluno_id: int) -> bool:
        stmt = select(Solicitacao.id).where(
            Solicitacao.aluno_id == aluno_id,
            Solicitacao.status == SolicitacaoStatus.ACEITA,
        )
        return self.db.scalars(stmt).first() is not None

    def aceitar(
        self, solicitacao: Solicitacao, trilha: Trilha
    ) -> Solicitacao:
        solicitacao.trilha_aceita = trilha
        solicitacao.status = SolicitacaoStatus.ACEITA
        solicitacao.resolvido_em = datetime.now()
        self.db.commit()
        self.db.refresh(solicitacao)
        return solicitacao
