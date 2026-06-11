from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from server.models.enums import SolicitacaoStatus
from server.models.solicitacao import Solicitacao


class SolicitacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def agregar_por_trilha(
        self, periodo_inicio: datetime, periodo_fim: datetime
    ) -> list[tuple[int, SolicitacaoStatus, int]]:
        stmt = (
            select(
                Solicitacao.trilha_sugerida_id,
                Solicitacao.status,
                func.count(Solicitacao.id),
            )
            .where(
                Solicitacao.resolvido_em.is_not(None),
                Solicitacao.resolvido_em >= periodo_inicio,
                Solicitacao.resolvido_em <= periodo_fim,
                Solicitacao.status.in_(
                    [SolicitacaoStatus.ACEITA, SolicitacaoStatus.REJEITADA]
                ),
            )
            .group_by(Solicitacao.trilha_sugerida_id, Solicitacao.status)
        )
        return list(self.db.execute(stmt).all())
