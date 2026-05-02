from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.user import User


class Aluno(Base):
    __tablename__ = "alunos"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    cartao_ufrgs: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    semestre_ingresso: Mapped[str] = mapped_column(String(7), nullable=False)

    user: Mapped[User] = relationship(back_populates="aluno")
