from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.schemas.trilha import TrilhaCreate, TrilhaResponse, TrilhaUpdate
from server.services.auth_service import require_roles
from server.services.trilha_service import TrilhaService


class TrilhaController:
    def __init__(self):
        self.router = APIRouter(prefix="/trilhas", tags=["trilhas"])
        comgrad_only = [require_roles(UserRole.COMGRAD)]
        comgrad_errors = {401: UNAUTHORIZED_401, 403: FORBIDDEN_403}
        self.router.add_api_route(
            "/get",
            self.get_trilhas,
            methods=["GET"],
            response_model=list[TrilhaResponse],
            summary="Pesquisar trilhas acadêmicas",
            description=(
                "Lista todas as trilhas ativas. Aceita filtro opcional `disciplina` "
                "que faz *fuzzy matching* (insensível a acento e capitalização) "
                "contra o nome das disciplinas — retorna trilhas que contenham "
                "ao menos uma disciplina com similaridade ≥ 65%."
            ),
        )
        self.router.add_api_route(
            "/create",
            self.criar_trilha,
            methods=["POST"],
            response_model=TrilhaResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=comgrad_only,
            summary="Cadastrar nova trilha",
            description=(
                "Cria uma trilha acadêmica nova com nome, resumo, lista de "
                "disciplinas e **pesos do questionário vocacional**.\n\n"
                "**Regras:**\n"
                "- Todas as disciplinas referenciadas precisam existir e estar "
                "ativas (400 listando os ids inválidos caso contrário).\n"
                "- `pesos` precisa cobrir **exatamente** as perguntas ativas do "
                "sistema — sem faltas e sem ids inválidos. Use `peso=0` quando "
                "a pergunta não pontua nesta trilha. Sem perguntas ativas no "
                "sistema, o cadastro é bloqueado.\n"
                "- Cada `peso` está no intervalo `[0.0, 1.0]`."
            ),
            responses={**comgrad_errors, 400: BAD_REQUEST_400},
        )
        self.router.add_api_route(
            "/update/{trilha_id}",
            self.editar_trilha,
            methods=["PATCH"],
            response_model=TrilhaResponse,
            dependencies=comgrad_only,
            summary="Editar trilha existente",
            description=(
                "Atualização parcial: apenas os campos enviados são alterados.\n\n"
                "Quando `pesos` é enviado, **substitui completamente** os pesos "
                "atuais da trilha e precisa cobrir exatamente as perguntas ativas "
                "(mesma regra do cadastro). Quando omitido, os pesos atuais ficam "
                "intactos."
            ),
            responses={**comgrad_errors, 400: BAD_REQUEST_400, 404: NOT_FOUND_404},
        )
        self.router.add_api_route(
            "/delete/{trilha_id}",
            self.excluir_trilha,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=comgrad_only,
            summary="Excluir trilha (soft delete)",
            description=(
                "Marca a trilha como inativa (`is_active=false`). Os dados ficam "
                "preservados no banco para manter histórico de aceites/rejeições."
            ),
            responses={**comgrad_errors, 404: NOT_FOUND_404},
        )

    def get_trilhas(
        self,
        disciplina: str | None = None,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.pesquisar(disciplina)

    def criar_trilha(
        self,
        payload: TrilhaCreate,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.cadastrar(
            nome=payload.nome,
            resumo=payload.resumo,
            disciplinas_ids=payload.disciplinas_ids,
            pesos=payload.pesos,
        )

    def editar_trilha(
        self,
        trilha_id: int,
        payload: TrilhaUpdate,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.editar(
            trilha_id,
            nome=payload.nome,
            resumo=payload.resumo,
            disciplinas_ids=payload.disciplinas_ids,
            pesos=payload.pesos,
        )

    def excluir_trilha(
        self,
        trilha_id: int,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        service.excluir(trilha_id)
