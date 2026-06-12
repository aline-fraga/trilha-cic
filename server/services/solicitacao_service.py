from fastapi import HTTPException
from sqlalchemy.orm import Session

from server.models.enums import SolicitacaoStatus
from server.models.solicitacao import Solicitacao
from server.repositories.solicitacao_repository import SolicitacaoRepository


class SolicitacaoService:
    def __init__(self, db: Session):
        self.solicitacao_repo = SolicitacaoRepository(db)

    def listar(
        self,
        aluno_id: int | None = None,
        status: SolicitacaoStatus | None = None,
    ) -> list[Solicitacao]:
        return self.solicitacao_repo.listar(aluno_id=aluno_id, status=status)

    def obter(self, solicitacao_id: int) -> Solicitacao:
        solicitacao = self.solicitacao_repo.obter(solicitacao_id)
        if solicitacao is None:
            raise HTTPException(
                status_code=404, detail="Solicitação não encontrada."
            )
        return solicitacao

    def aceitar(
        self, solicitacao_id: int, aluno_id: int, trilha_id: int
    ) -> Solicitacao:
        solicitacao = self.obter(solicitacao_id)

        if solicitacao.aluno_id != aluno_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        if solicitacao.status != SolicitacaoStatus.PENDENTE:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Solicitação já resolvida — status atual: "
                    f"{solicitacao.status.value}."
                ),
            )

        if self.solicitacao_repo.existe_aceita_para_aluno(aluno_id):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Aluno já possui uma trilha aceita. "
                    "Apenas uma trilha aceita por aluno é permitida."
                ),
            )

        trilha_escolhida = next(
            (t for t in solicitacao.trilhas_candidatas if t.id == trilha_id),
            None,
        )
        if trilha_escolhida is None:
            ids_validos = [t.id for t in solicitacao.trilhas_candidatas]
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Trilha {trilha_id} não está entre as candidatas desta "
                    f"solicitação. Candidatas válidas: {ids_validos}."
                ),
            )

        return self.solicitacao_repo.aceitar(solicitacao, trilha_escolhida)
