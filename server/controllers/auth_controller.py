from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.schemas.responses import UNAUTHORIZED_401
from server.schemas.user import LoginRequest, TokenResponse, UserInfo
from server.services.auth_service import AuthService, get_current_user


class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=TokenResponse,
            summary="Autenticar usuário",
            description=(
                "Recebe e-mail e senha; retorna um token JWT (`access_token`) "
                "válido por 8 horas. O token deve ser enviado como "
                "`Authorization: Bearer <token>` nos endpoints protegidos."
            ),
            responses={401: UNAUTHORIZED_401},
        )
        self.router.add_api_route(
            "/me",
            self.me,
            methods=["GET"],
            response_model=UserInfo,
            summary="Obter dados do usuário autenticado",
            description=(
                "Retorna os dados do usuário associado ao token Bearer. "
                "Inclui `cartao_ufrgs` se o usuário tiver papel ALUNO."
            ),
            responses={401: UNAUTHORIZED_401},
        )

    def login(self, body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
        service = AuthService(db)
        user = service.autenticar(body.email, body.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
            )
        return TokenResponse(access_token=service.criar_access_token(user.id))

    def me(self, current_user: User = Depends(get_current_user)) -> UserInfo:
        cartao = current_user.aluno.cartao_ufrgs if current_user.aluno else None
        return UserInfo(
            id=current_user.id,
            nome=current_user.nome,
            email=current_user.email,
            role=current_user.role,
            cartao_ufrgs=cartao,
        )
