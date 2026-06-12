from fastapi import HTTPException
from sqlalchemy.orm import Session

from server.models import Chamado
from server.models.enums import ChamadoStatus
from server.repositories.chamado_repository import ChamadoRepository
from server.schemas.chamado import ChamadoCreate


class ChamadoService:
    def __init__(self, db: Session):
        self.chamado_repo = ChamadoRepository(db)

    def listar(
        self, status: str | None = None, tipo: str | None = None
    ) -> list[Chamado]:
        return self.chamado_repo.listar(status=status, tipo=tipo)

    def buscar(self, id: int) -> Chamado | None:
        chamado = self.chamado_repo.buscar(id)
        if not chamado:
            raise HTTPException(status_code=404, detail="Chamado não encontrado.")
        return chamado

    def criar(self, dados: ChamadoCreate, aluno_id: int):
        chamados_abertos = self.chamado_repo.listar(status=ChamadoStatus.ABERTO.value)
        if any(
            c.aluno_id == aluno_id and c.tipo == dados.tipo for c in chamados_abertos
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Você já possui um chamado em aberto do tipo {dados.tipo.value}. "
                    "Aguarde a resposta antes de abrir outro do mesmo tipo."
                ),
            )

        if not dados.mensagem.strip():
            raise HTTPException(
                status_code=400, detail="A mensagem não pode estar em branco."
            )

        novo_chamado = Chamado(
            aluno_id=aluno_id,
            assunto=dados.assunto,
            mensagem=dados.mensagem,
            tipo=dados.tipo,
        )

        return self.chamado_repo.salvar(novo_chamado)

    def atualizar(self, id: int, resposta: str, respondido_por_id: int):
        chamado = self.buscar(id)

        chamado.resposta = resposta
        chamado.status = ChamadoStatus.FECHADO
        chamado.respondido_por_id = respondido_por_id

        return self.chamado_repo.salvar(chamado)
