from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from server.database import Base
from server.models.enums import SolicitacaoStatus


class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    trilha_sugerida_id: Mapped[int] = mapped_column(
        ForeignKey("trilhas.id"), nullable=False
    )
    status: Mapped[SolicitacaoStatus] = mapped_column(
        Enum(SolicitacaoStatus),
        nullable=False,
        server_default=SolicitacaoStatus.PENDENTE.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    resolvido_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
