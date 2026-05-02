from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.disciplina import Disciplina

trilha_disciplinas = Table(
    "trilha_disciplinas",
    Base.metadata,
    Column("trilha_id", ForeignKey("trilhas.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "disciplina_id",
        ForeignKey("disciplinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Trilha(Base):
    __tablename__ = "trilhas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    resumo: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    disciplinas: Mapped[List[Disciplina]] = relationship(
        secondary=trilha_disciplinas, back_populates="trilhas"
    )
