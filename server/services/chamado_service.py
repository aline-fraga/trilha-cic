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

    def existe_aberto_para_aluno(self, aluno_id: int) -> bool:
        return self.chamado_repo.existe_aberto_para_aluno(aluno_id)

    def criar(self, dados: ChamadoCreate, aluno_id: int):
        if self.chamado_repo.existe_aberto_para_aluno(aluno_id, dados.tipo):
            detalhe_tipo = (
                "para sugestão de trilha"
                if dados.tipo.value == "NOVA_TRILHA"
                else f"do tipo {dados.tipo.value}"
            )
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Você já possui um chamado em aberto {detalhe_tipo}. "
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

    def editar_mensagem(self, id: int, aluno_id: int, nova_mensagem: str):
        chamado = self.buscar(id)

        if chamado.aluno_id != aluno_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        if chamado.status != ChamadoStatus.ABERTO:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Apenas chamados em ABERTO podem ter a mensagem editada — "
                    f"status atual: {chamado.status.value}."
                ),
            )

        if not nova_mensagem.strip():
            raise HTTPException(
                status_code=400, detail="A mensagem não pode estar em branco."
            )

        chamado.mensagem = nova_mensagem
        return self.chamado_repo.salvar(chamado)
