from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.schemas.user import UserAdminResponse, UserCreate, UserUpdate
from server.services.auth_service import require_roles
from server.services.user_service import UserService


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["users"])
        admin_only = [require_roles(UserRole.ADMIN)]

        self.router.add_api_route(
            "/get",
            self.listar_usuarios,
            methods=["GET"],
            response_model=list[UserAdminResponse],
            dependencies=admin_only,
        )
        self.router.add_api_route(
            "/get/{user_id}",
            self.obter_usuario,
            methods=["GET"],
            response_model=UserAdminResponse,
            dependencies=admin_only,
        )
        self.router.add_api_route(
            "/create",
            self.criar_usuario,
            methods=["POST"],
            response_model=UserAdminResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=admin_only,
        )
        self.router.add_api_route(
            "/update/{user_id}",
            self.editar_usuario,
            methods=["PATCH"],
            response_model=UserAdminResponse,
            dependencies=admin_only,
        )
        self.router.add_api_route(
            "/delete/{user_id}",
            self.excluir_usuario,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=admin_only,
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
