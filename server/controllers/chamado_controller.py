from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.models.user import User
from server.schemas.chamado import (
    ChamadoCreate,
    ChamadoEditMensagem,
    ChamadoResponder,
    ChamadoResponse,
)
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.services.auth_service import get_current_user, require_roles
from server.services.chamado_service import ChamadoService
from server.services.user_service import UserService


class ChamadoController:
    def __init__(self):
        self.router = APIRouter(prefix="/chamados", tags=["chamados"])

        self.router.add_api_route(
            "",
            self.abrir_chamado,
            methods=["POST"],
            response_model=ChamadoResponse,
            status_code=201,
            dependencies=[require_roles(UserRole.ALUNO)],
            summary="Abrir novo chamado (ALUNO)",
            description=(
                "Registra um chamado em nome do aluno autenticado, com status "
                "inicial `ABERTO`.\n\n"
                "**Regras:**\n"
                "- O aluno só pode ter **um chamado em aberto por tipo** "
                "(`TRILHA_REJEITADA` ou `NOVA_TRILHA`); tentar abrir um segundo "
                "do mesmo tipo retorna 400.\n"
                "- `mensagem` não pode ser vazia (após `strip`)."
            ),
            responses={
                400: BAD_REQUEST_400,
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
            },
        )

        self.router.add_api_route(
            "",
            self.listar_chamados,
            methods=["GET"],
            response_model=list[ChamadoResponse],
            dependencies=[Depends(get_current_user)],
            summary="Listar chamados",
            description=(
                "Retorna os chamados ordenados por data de criação decrescente.\n\n"
                "**Visibilidade por papel:**\n"
                "- `ALUNO` — vê apenas os próprios chamados (filtro implícito por "
                "`aluno_id` do token).\n"
                "- `COMGRAD` / `ADMIN` — vê todos os chamados de todos os alunos.\n\n"
                "**Filtros opcionais (combináveis):**\n"
                "- `status`: `ABERTO` ou `FECHADO`.\n"
                "- `tipo`: `TRILHA_REJEITADA` ou `NOVA_TRILHA`."
            ),
            responses={401: UNAUTHORIZED_401},
        )

        self.router.add_api_route(
            "/{chamado_id}",
            self.editar_mensagem_chamado,
            methods=["PATCH"],
            response_model=ChamadoResponse,
            dependencies=[require_roles(UserRole.ALUNO)],
            summary="Editar mensagem do chamado (ALUNO)",
            description=(
                "Permite ao aluno **dono** do chamado atualizar a `mensagem` "
                "enquanto o chamado ainda estiver `ABERTO`.\n\n"
                "**Regras:**\n"
                "- Apenas o aluno que abriu o chamado pode editar (403 caso "
                "contrário).\n"
                "- Só é possível editar com `status = ABERTO`. Chamado já "
                "respondido/`FECHADO` retorna 400.\n"
                "- `mensagem` não pode ser vazia (após `strip`).\n\n"
                "Demais campos (`tipo`, `assunto`, `status`, etc.) são "
                "imutáveis por esta rota."
            ),
            responses={
                400: BAD_REQUEST_400,
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
                404: NOT_FOUND_404,
            },
        )

        self.router.add_api_route(
            "/{chamado_id}/responder",
            self.responder_chamado,
            methods=["PUT"],
            response_model=ChamadoResponse,
            dependencies=[require_roles(UserRole.COMGRAD, UserRole.ADMIN)],
            summary="Responder chamado (COMGRAD/ADMIN)",
            description=(
                "Registra a resposta da COMGRAD e encerra o chamado: status muda "
                "para `FECHADO`, `respondido_por_id` recebe o id do autor do token "
                "e `respondido_em` é preenchido com o timestamp atual."
            ),
            responses={
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
                404: NOT_FOUND_404,
            },
        )

    def abrir_chamado(
        self,
        dados: ChamadoCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = ChamadoService(db)
        user_service = UserService(db)

        c = service.criar(dados, current_user.id)
        aluno = user_service.obter(c.aluno_id)

        c_dict = {
            "id": c.id,
            "aluno_id": c.aluno_id,
            "aluno_nome": aluno.nome if aluno else "Desconhecido",
            "tipo": c.tipo,
            "assunto": c.assunto,
            "mensagem": c.mensagem,
            "status": c.status,
            "resposta": c.resposta,
            "respondido_em": c.respondido_em,
            "trilha_id": c.trilha_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        return ChamadoResponse(**c_dict)

    def listar_chamados(
        self,
        status: str | None = None,
        tipo: str | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = ChamadoService(db)
        user_service = UserService(db)

        chamados_db = service.listar(status=status, tipo=tipo)
        
        if current_user.role == UserRole.ALUNO:
            chamados_db = [c for c in chamados_db if c.aluno_id == current_user.id]

        usuarios_cache = {}
        res = []
        for c in chamados_db:
            if c.aluno_id not in usuarios_cache:
                usuarios_cache[c.aluno_id] = user_service.obter(c.aluno_id)
            aluno = usuarios_cache[c.aluno_id]

            c_dict = {
                "id": c.id,
                "aluno_id": c.aluno_id,
                "aluno_nome": aluno.nome if aluno else "Desconhecido",
                "tipo": c.tipo,
                "assunto": c.assunto,
                "mensagem": c.mensagem,
                "status": c.status,
                "resposta": c.resposta,
                "respondido_em": c.respondido_em,
                "trilha_id": c.trilha_id,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
            }
            res.append(ChamadoResponse(**c_dict))
            
        return res

    def editar_mensagem_chamado(
        self,
        chamado_id: int,
        dados: ChamadoEditMensagem,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = ChamadoService(db)
        user_service = UserService(db)

        c = service.editar_mensagem(chamado_id, current_user.id, dados.mensagem)
        aluno = user_service.obter(c.aluno_id)

        c_dict = {
            "id": c.id,
            "aluno_id": c.aluno_id,
            "aluno_nome": aluno.nome if aluno else "Desconhecido",
            "tipo": c.tipo,
            "assunto": c.assunto,
            "mensagem": c.mensagem,
            "status": c.status,
            "resposta": c.resposta,
            "respondido_em": c.respondido_em,
            "trilha_id": c.trilha_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        return ChamadoResponse(**c_dict)

    def responder_chamado(
        self,
        chamado_id: int,
        dados: ChamadoResponder,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = ChamadoService(db)
        user_service = UserService(db)
        
        c = service.atualizar(chamado_id, dados.resposta, current_user.id)
        aluno = user_service.obter(c.aluno_id)
        
        c_dict = {
            "id": c.id,
            "aluno_id": c.aluno_id,
            "aluno_nome": aluno.nome if aluno else "Desconhecido",
            "tipo": c.tipo,
            "assunto": c.assunto,
            "mensagem": c.mensagem,
            "status": c.status,
            "resposta": c.resposta,
            "respondido_em": c.respondido_em,
            "trilha_id": c.trilha_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        return ChamadoResponse(**c_dict)
