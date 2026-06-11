from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.schemas.responses import (
    BAD_REQUEST_400,
    CONFLICT_409,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.schemas.user import UserAdminResponse, UserCreate, UserUpdate
from server.services.auth_service import require_roles
from server.services.user_service import UserService


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        admin_only = [require_roles(UserRole.ADMIN)]
        admin_errors = {401: UNAUTHORIZED_401, 403: FORBIDDEN_403}

        self.router.add_api_route(
            "/get",
            self.listar_usuarios,
            methods=["GET"],
            response_model=list[UserAdminResponse],
            dependencies=admin_only,
            summary="Listar usuários (admin)",
            description=(
                "Lista todos os usuários cadastrados, ordenados por data de criação "
                "decrescente. Aceita filtros opcionais `role` "
                "(`ALUNO`/`COMGRAD`/`ADMIN`) e `is_active` (`true`/`false`)."
            ),
            responses={**admin_errors},
        )
        self.router.add_api_route(
            "/get/{user_id}",
            self.obter_usuario,
            methods=["GET"],
            response_model=UserAdminResponse,
            dependencies=admin_only,
            summary="Obter usuário por ID (admin)",
            description=(
                "Retorna os dados completos de um usuário. Quando o usuário tem "
                "papel ALUNO, o objeto `aluno` é incluído na resposta."
            ),
            responses={**admin_errors, 404: NOT_FOUND_404},
        )
        self.router.add_api_route(
            "/create",
            self.criar_usuario,
            methods=["POST"],
            response_model=UserAdminResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=admin_only,
            summary="Criar novo usuário (admin)",
            description=(
                "Cria um novo usuário do sistema. A senha é armazenada com hash bcrypt.\n\n"
                "**Regras:**\n"
                "- `role=ALUNO` exige o objeto `aluno` com `cartao_ufrgs` e `semestre_ingresso`.\n"
                "- `role=COMGRAD` ou `role=ADMIN` deve **omitir** o objeto `aluno`.\n"
                "- O `email` deve ser único no sistema."
            ),
            responses={
                **admin_errors,
                400: BAD_REQUEST_400,
                409: CONFLICT_409,
            },
        )
        self.router.add_api_route(
            "/update/{user_id}",
            self.editar_usuario,
            methods=["PATCH"],
            response_model=UserAdminResponse,
            dependencies=admin_only,
            summary="Editar usuário existente (admin)",
            description=(
                "Atualização parcial — apenas os campos enviados são modificados. "
                "O campo `role` **não pode ser alterado** (não faz parte do payload). "
                "O objeto `aluno` só pode ser editado quando o usuário já tem papel ALUNO."
            ),
            responses={
                **admin_errors,
                400: BAD_REQUEST_400,
                404: NOT_FOUND_404,
                409: CONFLICT_409,
            },
        )
        self.router.add_api_route(
            "/delete/{user_id}",
            self.excluir_usuario,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=admin_only,
            summary="Desativar usuário (admin)",
            description=(
                "Soft delete: marca o usuário com `is_active=false`. O registro "
                "permanece no banco para preservar referências em chamados, "
                "solicitações e relatórios históricos."
            ),
            responses={**admin_errors, 404: NOT_FOUND_404},
        )

    def listar_usuarios(
        self,
        role: UserRole | None = None,
        is_active: bool | None = None,
        db: Session = Depends(get_db),
    ):
        service = UserService(db)
        return service.listar(role=role, is_active=is_active)

    def obter_usuario(
        self,
        user_id: int,
        db: Session = Depends(get_db),
    ):
        service = UserService(db)
        return service.obter(user_id)

    def criar_usuario(
        self,
        payload: UserCreate,
        db: Session = Depends(get_db),
    ):
        service = UserService(db)
        return service.cadastrar(
            email=payload.email,
            nome=payload.nome,
            password=payload.password,
            role=payload.role,
            aluno=payload.aluno,
        )

    def editar_usuario(
        self,
        user_id: int,
        payload: UserUpdate,
        db: Session = Depends(get_db),
    ):
        service = UserService(db)
        return service.editar(
            user_id,
            email=payload.email,
            nome=payload.nome,
            is_active=payload.is_active,
            aluno=payload.aluno,
        )

    def excluir_usuario(
        self,
        user_id: int,
        db: Session = Depends(get_db),
    ):
        service = UserService(db)
        service.excluir(user_id)
