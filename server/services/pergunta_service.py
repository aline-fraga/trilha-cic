from fastapi import HTTPException
from sqlalchemy.orm import Session

from server.models import Pergunta
from server.repositories.pergunta_repository import PerguntaRepository
from server.schemas.pergunta import PerguntaCreate, PerguntaUpdate


class PerguntaService:
    def __init__(self, db: Session):
        self.repo = PerguntaRepository(db)

    def listar(self, is_active: bool | None = None) -> list[Pergunta]:
        return self.repo.listar(is_active=is_active)

    def listar_ativas(self) -> list[Pergunta]:
        return self.repo.listar_ativas()

    def obter(self, pergunta_id: int) -> Pergunta:
        pergunta = self.repo.obter(pergunta_id)
        if pergunta is None or not pergunta.is_active:
            raise HTTPException(
                status_code=404, detail="Pergunta não encontrada"
            )
        return pergunta

    def criar(self, data: PerguntaCreate) -> Pergunta:
        pergunta = Pergunta(
            enunciado=data.enunciado,
            tipo=data.tipo,
            ordem=data.ordem,
        )
        return self.repo.criar(pergunta)

    def atualizar(
        self, pergunta_id: int, data: PerguntaUpdate
    ) -> Pergunta:
        pergunta = self.obter(pergunta_id)
        return self.repo.atualizar(
            pergunta,
            enunciado=data.enunciado,
            tipo=data.tipo,
            ordem=data.ordem,
        )

    def excluir(self, pergunta_id: int) -> None:
        pergunta = self.obter(pergunta_id)
        self.repo.inativar(pergunta)
