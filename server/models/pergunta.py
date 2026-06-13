from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.enums import PerguntaTipo


class Pergunta(Base):
    __tablename__ = "perguntas"

    id: Mapped[int] = mapped_column(primary_key=True)
    enunciado: Mapped[str] = mapped_column(String(500), nullable=False)
    tipo: Mapped[PerguntaTipo] = mapped_column(nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    pesos: Mapped[List["PerguntaTrilhaPeso"]] = relationship(
        back_populates="pergunta", cascade="all, delete-orphan"
    )


class PerguntaTrilhaPeso(Base):
    __tablename__ = "pergunta_trilha_pesos"

    pergunta_id: Mapped[int] = mapped_column(
        ForeignKey("perguntas.id", ondelete="CASCADE"), primary_key=True
    )
    trilha_id: Mapped[int] = mapped_column(
        ForeignKey("trilhas.id", ondelete="CASCADE"), primary_key=True
    )
    peso: Mapped[float] = mapped_column(Float, nullable=False)

    pergunta: Mapped[Pergunta] = relationship(back_populates="pesos")
    trilha: Mapped["Trilha"] = relationship(back_populates="pesos_perguntas")  # noqa: F821
