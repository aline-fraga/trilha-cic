from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.chamado import Chamado
from server.models.disciplina import Disciplina

sugestao_trilha_disciplinas = Table(
    "sugestao_trilha_disciplinas",
    Base.metadata,
    Column(
        "sugestao_id",
        ForeignKey("sugestoes_trilha.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "disciplina_id",
        ForeignKey("disciplinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class SugestaoTrilha(Base):
    __tablename__ = "sugestoes_trilha"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    chamado_id: Mapped[int] = mapped_column(
        ForeignKey("chamados.id"), nullable=False, unique=True
    )
    nome_proposto: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    chamado: Mapped[Chamado] = relationship()
    disciplinas: Mapped[List[Disciplina]] = relationship(
        secondary=sugestao_trilha_disciplinas, back_populates="sugestoes_trilha"
    )
