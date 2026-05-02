from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from server.database import Base
from server.models.enums import ChamadoStatus, ChamadoTipo


class Chamado(Base):
    __tablename__ = "chamados"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tipo: Mapped[ChamadoTipo] = mapped_column(Enum(ChamadoTipo), nullable=False)
    assunto: Mapped[str] = mapped_column(String(200), nullable=False)
    mensagem: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ChamadoStatus] = mapped_column(
        Enum(ChamadoStatus), nullable=False, server_default=ChamadoStatus.ABERTO.value
    )
    resposta: Mapped[str | None] = mapped_column(Text, nullable=True)
    trilha_id: Mapped[int | None] = mapped_column(
        ForeignKey("trilhas.id"), nullable=True
    )
    respondido_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    respondido_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
