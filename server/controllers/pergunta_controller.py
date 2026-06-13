from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.schemas.pergunta import (
    PerguntaCreate,
    PerguntaResponse,
    PerguntaUpdate,
)
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.services.auth_service import get_current_user, require_roles
from server.services.pergunta_service import PerguntaService


class PerguntaController:
    def __init__(self):
        self.router = APIRouter(prefix="/perguntas", tags=["perguntas"])
        comgrad_only = [require_roles(UserRole.COMGRAD)]
        comgrad_errors = {401: UNAUTHORIZED_401, 403: FORBIDDEN_403}

        self.router.add_api_route(
            "/get",
            self.listar_perguntas,
            methods=["GET"],
            response_model=list[PerguntaResponse],
            dependencies=[Depends(get_current_user)],
            summary="Listar perguntas do questionário vocacional",
            description=(
                "Lista as perguntas do questionário usado em `POST "
                "/solicitacoes/create` (UC03), ordenadas por `ordem` e `id`.\n\n"
                "Aceita filtro opcional `is_active` (`true`/`false`). Sem o "
                "filtro, retorna ativas e inativas. Acessível a qualquer "
                "usuário autenticado."
            ),
            responses={401: UNAUTHORIZED_401},
        )

        self.router.add_api_route(
            "/get/{pergunta_id}",
            self.obter_pergunta,
            methods=["GET"],
            response_model=PerguntaResponse,
            dependencies=[Depends(get_current_user)],
            summary="Obter pergunta por ID",
            description=(
                "Retorna uma pergunta ativa. Perguntas inativas retornam 404. "
                "Acessível a qualquer usuário autenticado."
            ),
            responses={401: UNAUTHORIZED_401, 404: NOT_FOUND_404},
        )

        self.router.add_api_route(
            "/create",
            self.criar_pergunta,
            methods=["POST"],
            response_model=PerguntaResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=comgrad_only,
            summary="Cadastrar nova pergunta (COMGRAD)",
            description=(
                "Cadastra uma pergunta no questionário vocacional.\n\n"
                "**Campos obrigatórios:** `enunciado`, `tipo` (`CONCEITUAL` "
                "ou `PRATICA`), `ordem` (≥ 0).\n\n"
                "**Nota:** Após criar uma pergunta nova, as trilhas existentes "
                "passam a tê-la como peso ausente (= 0 no algoritmo). Pra que "
                "a pergunta passe a influenciar uma trilha, edite a trilha "
                "com `pesos` atualizados."
            ),
            responses={**comgrad_errors, 400: BAD_REQUEST_400},
        )

        self.router.add_api_route(
            "/update/{pergunta_id}",
            self.atualizar_pergunta,
            methods=["PATCH"],
            response_model=PerguntaResponse,
            dependencies=comgrad_only,
            summary="Atualizar pergunta (COMGRAD)",
            description=(
                "Atualização parcial: apenas os campos enviados são alterados. "
                "Os pesos das trilhas em relação a essa pergunta são preservados."
            ),
            responses={
                **comgrad_errors,
                400: BAD_REQUEST_400,
                404: NOT_FOUND_404,
            },
        )

        self.router.add_api_route(
            "/delete/{pergunta_id}",
            self.excluir_pergunta,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=comgrad_only,
            summary="Excluir pergunta (COMGRAD)",
            description=(
                "Desativa a pergunta (`is_active=false`). Exclusão lógica; "
                "perguntas inativas saem do questionário e deixam de influenciar "
                "o algoritmo de sugestão (mesmo com pesos cadastrados nas "
                "trilhas, esses pesos passam a ser ignorados)."
            ),
            responses={**comgrad_errors, 404: NOT_FOUND_404},
        )

    def listar_perguntas(
        self,
        is_active: bool | None = None,
        db: Session = Depends(get_db),
    ):
        return PerguntaService(db).listar(is_active=is_active)

    def obter_pergunta(
        self,
        pergunta_id: int,
        db: Session = Depends(get_db),
    ):
        return PerguntaService(db).obter(pergunta_id)

    def criar_pergunta(
        self,
        payload: PerguntaCreate,
        db: Session = Depends(get_db),
    ):
        return PerguntaService(db).criar(payload)

    def atualizar_pergunta(
        self,
        pergunta_id: int,
        payload: PerguntaUpdate,
        db: Session = Depends(get_db),
    ):
        return PerguntaService(db).atualizar(pergunta_id, payload)

    def excluir_pergunta(
        self,
        pergunta_id: int,
        db: Session = Depends(get_db),
    ):
        PerguntaService(db).excluir(pergunta_id)
