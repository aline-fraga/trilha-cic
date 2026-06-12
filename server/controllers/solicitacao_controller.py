from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import SolicitacaoStatus, UserRole
from server.models.solicitacao import Solicitacao
from server.models.user import User
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.schemas.solicitacao import AceitarTrilhaRequest, SolicitacaoResponse
from server.services.auth_service import get_current_user, require_roles
from server.services.solicitacao_service import SolicitacaoService
from server.services.user_service import UserService


class SolicitacaoController:
    def __init__(self):
        self.router = APIRouter(prefix="/solicitacoes", tags=["solicitacoes"])

        self.router.add_api_route(
            "/get",
            self.listar_solicitacoes,
            methods=["GET"],
            response_model=list[SolicitacaoResponse],
            dependencies=[Depends(get_current_user)],
            summary="Listar solicitações de trilha",
            description=(
                "Retorna as solicitações ordenadas por data de criação "
                "decrescente.\n\n"
                "**Visibilidade por papel:**\n"
                "- `ALUNO` — vê apenas as próprias solicitações.\n"
                "- `COMGRAD` / `ADMIN` — vê todas.\n\n"
                "**Filtro opcional:** `status` em "
                "`PENDENTE`, `ACEITA` ou `REJEITADA`."
            ),
            responses={401: UNAUTHORIZED_401},
        )

        self.router.add_api_route(
            "/get/{solicitacao_id}",
            self.obter_solicitacao,
            methods=["GET"],
            response_model=SolicitacaoResponse,
            dependencies=[Depends(get_current_user)],
            summary="Obter solicitação por ID",
            description=(
                "Retorna os dados completos de uma solicitação, incluindo a "
                "lista de trilhas candidatas (sugeridas) e — se já aceita — a "
                "trilha escolhida. ALUNO só pode obter solicitações próprias "
                "(403 caso contrário)."
            ),
            responses={
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
                404: NOT_FOUND_404,
            },
        )

        self.router.add_api_route(
            "/aceitar/{solicitacao_id}",
            self.aceitar_solicitacao,
            methods=["PATCH"],
            response_model=SolicitacaoResponse,
            dependencies=[require_roles(UserRole.ALUNO)],
            summary="Aceitar trilha sugerida (ALUNO)",
            description=(
                "Marca a solicitação como `ACEITA` e registra qual das trilhas "
                "candidatas foi escolhida em `trilha_aceita`. Preenche também "
                "`resolvido_em` com o timestamp atual.\n\n"
                "**Regras:**\n"
                "- A solicitação precisa pertencer ao aluno autenticado (403 "
                "caso contrário).\n"
                "- A solicitação precisa estar em status `PENDENTE` "
                "(400 caso contrário).\n"
                "- O aluno **não pode** ter outra trilha já `ACEITA` "
                "(limite atual = 1 aceita por aluno; 400 caso contrário).\n"
                "- `trilha_id` deve estar entre as `trilhas_candidatas` da "
                "solicitação (400 caso contrário)."
            ),
            responses={
                400: BAD_REQUEST_400,
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
                404: NOT_FOUND_404,
            },
        )

    def listar_solicitacoes(
        self,
        status: SolicitacaoStatus | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SolicitacaoService(db)
        aluno_filter = (
            current_user.id if current_user.role == UserRole.ALUNO else None
        )
        solicitacoes = service.listar(aluno_id=aluno_filter, status=status)
        user_service = UserService(db)
        cache: dict[int, User | None] = {}
        return [
            self._montar_response(s, user_service, cache) for s in solicitacoes
        ]

    def obter_solicitacao(
        self,
        solicitacao_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SolicitacaoService(db)
        solicitacao = service.obter(solicitacao_id)
        if (
            current_user.role == UserRole.ALUNO
            and solicitacao.aluno_id != current_user.id
        ):
            raise HTTPException(status_code=403, detail="Acesso negado")
        return self._montar_response(solicitacao, UserService(db))

    def aceitar_solicitacao(
        self,
        solicitacao_id: int,
        payload: AceitarTrilhaRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SolicitacaoService(db)
        solicitacao = service.aceitar(
            solicitacao_id=solicitacao_id,
            aluno_id=current_user.id,
            trilha_id=payload.trilha_id,
        )
        return self._montar_response(solicitacao, UserService(db))

    @staticmethod
    def _montar_response(
        solicitacao: Solicitacao,
        user_service: UserService,
        cache: dict[int, User | None] | None = None,
    ) -> SolicitacaoResponse:
        if cache is not None:
            if solicitacao.aluno_id not in cache:
                cache[solicitacao.aluno_id] = user_service.obter(
                    solicitacao.aluno_id
                )
            aluno = cache[solicitacao.aluno_id]
        else:
            aluno = user_service.obter(solicitacao.aluno_id)
        return SolicitacaoResponse(
            id=solicitacao.id,
            aluno_id=solicitacao.aluno_id,
            aluno_nome=aluno.nome if aluno else "Desconhecido",
            trilhas_candidatas=solicitacao.trilhas_candidatas,
            trilha_aceita=solicitacao.trilha_aceita,
            status=solicitacao.status,
            created_at=solicitacao.created_at,
            resolvido_em=solicitacao.resolvido_em,
        )
