from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.enums import SolicitacaoStatus
from server.models.trilha import Trilha

solicitacao_trilhas_candidatas = Table(
    "solicitacao_trilhas_candidatas",
    Base.metadata,
    Column(
        "solicitacao_id",
        ForeignKey("solicitacoes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "trilha_id",
        ForeignKey("trilhas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    trilha_aceita_id: Mapped[int | None] = mapped_column(
        ForeignKey("trilhas.id"), nullable=True
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

    trilha_aceita: Mapped[Trilha | None] = relationship(
        foreign_keys=[trilha_aceita_id]
    )
    trilhas_candidatas: Mapped[List[Trilha]] = relationship(
        secondary=solicitacao_trilhas_candidatas
    )
