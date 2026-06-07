from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.disciplina import Disciplina

curriculo_disciplinas = Table(
    "curriculo_disciplinas",
    Base.metadata,
    Column(
        "curriculo_id", ForeignKey("curriculos.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "disciplina_id",
        ForeignKey("disciplinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Curriculo(Base):
    __tablename__ = "curriculos"

    id: Mapped[int] = mapped_column(primary_key=True)
    curso: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    ano_vigencia: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    disciplinas: Mapped[List[Disciplina]] = relationship(
        secondary=curriculo_disciplinas, back_populates="curriculos"
    )
