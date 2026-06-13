from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.schemas.disciplina import (
    DisciplinaCreate,
    DisciplinaResponse,
    DisciplinaUpdate,
)
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.services.auth_service import get_current_user, require_roles
from server.services.disciplina_service import DisciplinaService


class DisciplinaController:
    def __init__(self):
        self.router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])
        comgrad_only = [require_roles(UserRole.COMGRAD)]
        comgrad_errors = {401: UNAUTHORIZED_401, 403: FORBIDDEN_403}

        self.router.add_api_route(
            "/get",
            self.listar_disciplinas,
            methods=["GET"],
            response_model=list[DisciplinaResponse],
            dependencies=[Depends(get_current_user)],
            summary="Listar disciplinas",
            description=(
                "Lista as disciplinas cadastradas, ordenadas por nome.\n\n"
                "Aceita filtro opcional `is_active` (`true`/`false`). Sem o "
                "filtro, retorna ativas e inativas. Acessível a qualquer "
                "usuário autenticado."
            ),
            responses={401: UNAUTHORIZED_401},
        )

        self.router.add_api_route(
            "/get/{disciplina_id}",
            self.obter_disciplina,
            methods=["GET"],
            response_model=DisciplinaResponse,
            dependencies=[Depends(get_current_user)],
            summary="Obter disciplina por ID",
            description=(
                "Retorna os dados completos de uma disciplina ativa. "
                "Disciplinas inativas retornam 404. Acessível a qualquer "
                "usuário autenticado."
            ),
            responses={401: UNAUTHORIZED_401, 404: NOT_FOUND_404},
        )

        self.router.add_api_route(
            "/create",
            self.criar_disciplina,
            methods=["POST"],
            response_model=DisciplinaResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=comgrad_only,
            summary="Cadastrar disciplina (COMGRAD)",
            description=(
                "Cria uma nova disciplina no catálogo. O `codigo` precisa ser "
                "único — retorna 400 se já existir.\n\n"
                "**Campos obrigatórios:** `nome`, `codigo`, `tipo` "
                "(`OBRIGATORIA` ou `ELETIVA`), `carga_horaria` (> 0)."
            ),
            responses={**comgrad_errors, 400: BAD_REQUEST_400},
        )

        self.router.add_api_route(
            "/update/{disciplina_id}",
            self.atualizar_disciplina,
            methods=["PUT"],
            response_model=DisciplinaResponse,
            dependencies=comgrad_only,
            summary="Atualizar disciplina (COMGRAD)",
            description=(
                "Atualiza campos da disciplina. Apenas campos enviados são "
                "alterados. Mudar `codigo` para um já existente retorna 400."
            ),
            responses={
                **comgrad_errors,
                400: BAD_REQUEST_400,
                404: NOT_FOUND_404,
            },
        )

        self.router.add_api_route(
            "/delete/{disciplina_id}",
            self.excluir_disciplina,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=comgrad_only,
            summary="Excluir disciplina (COMGRAD)",
            description=(
                "Desativa a disciplina (`is_active=false`). Exclusão lógica; "
                "os dados ficam preservados no banco para manter histórico "
                "em trilhas e currículos passados."
            ),
            responses={**comgrad_errors, 404: NOT_FOUND_404},
        )

    def listar_disciplinas(
        self,
        is_active: bool | None = None,
        db: Session = Depends(get_db),
    ):
        return DisciplinaService(db).listar(is_active=is_active)

    def obter_disciplina(
        self,
        disciplina_id: int,
        db: Session = Depends(get_db),
    ):
        return DisciplinaService(db).buscar(disciplina_id)

    def criar_disciplina(
        self,
        payload: DisciplinaCreate,
        db: Session = Depends(get_db),
    ):
        return DisciplinaService(db).criar(payload)

    def atualizar_disciplina(
        self,
        disciplina_id: int,
        payload: DisciplinaUpdate,
        db: Session = Depends(get_db),
    ):
        return DisciplinaService(db).atualizar(disciplina_id, payload)

    def excluir_disciplina(
        self,
        disciplina_id: int,
        db: Session = Depends(get_db),
    ):
        DisciplinaService(db).excluir(disciplina_id)
