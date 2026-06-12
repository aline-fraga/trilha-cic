from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models.aluno import Aluno


class AlunoRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter_por_user_id(self, user_id: int) -> Aluno | None:
        stmt = select(Aluno).where(Aluno.user_id == user_id)
        return self.db.scalar(stmt)

    def criar(
        self,
        *,
        user_id: int,
        cartao_ufrgs: str,
        semestre_ingresso: str,
    ) -> Aluno:
        aluno = Aluno(
            user_id=user_id,
            cartao_ufrgs=cartao_ufrgs,
            semestre_ingresso=semestre_ingresso,
        )
        self.db.add(aluno)
        self.db.commit()
        self.db.refresh(aluno)
        return aluno

    def atualizar(
        self,
        aluno: Aluno,
        *,
        cartao_ufrgs: str | None = None,
        semestre_ingresso: str | None = None,
    ) -> Aluno:
        if cartao_ufrgs is not None:
            aluno.cartao_ufrgs = cartao_ufrgs
        if semestre_ingresso is not None:
            aluno.semestre_ingresso = semestre_ingresso
        self.db.commit()
        self.db.refresh(aluno)
        return aluno
