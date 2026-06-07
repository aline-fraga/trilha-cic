from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.enums import DisciplinaTipo


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    tipo: Mapped[DisciplinaTipo] = mapped_column(Enum(DisciplinaTipo), nullable=False)
    link_plano_ensino: Mapped[str | None] = mapped_column(String(500), nullable=True)
    carga_horaria: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    trilhas: Mapped[List["Trilha"]] = relationship(  # noqa: F821
        secondary="trilha_disciplinas", back_populates="disciplinas"
    )
    curriculos: Mapped[List["Curriculo"]] = relationship(  # noqa: F821
        secondary="curriculo_disciplinas", back_populates="disciplinas"
    )
