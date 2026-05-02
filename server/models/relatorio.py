from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base


class Relatorio(Base):
    __tablename__ = "relatorios"

    id: Mapped[int] = mapped_column(primary_key=True)
    gerado_por_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    periodo_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    periodo_fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_solicitacoes: Mapped[int] = mapped_column(nullable=False)
    total_aceites: Mapped[int] = mapped_column(nullable=False)
    total_rejeicoes: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    itens: Mapped[List["RelatorioItem"]] = relationship(
        back_populates="relatorio", cascade="all, delete-orphan"
    )


class RelatorioItem(Base):
    __tablename__ = "relatorio_itens"

    id: Mapped[int] = mapped_column(primary_key=True)
    relatorio_id: Mapped[int] = mapped_column(
        ForeignKey("relatorios.id", ondelete="CASCADE"), nullable=False
    )
    trilha_id: Mapped[int] = mapped_column(ForeignKey("trilhas.id"), nullable=False)
    aceites: Mapped[int] = mapped_column(nullable=False, server_default="0")
    rejeicoes: Mapped[int] = mapped_column(nullable=False, server_default="0")

    relatorio: Mapped[Relatorio] = relationship(back_populates="itens")
