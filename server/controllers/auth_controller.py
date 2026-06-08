from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.schemas.user import LoginRequest, TokenResponse, UserInfo
from server.services.auth_service import authenticate_user, create_access_token, get_current_user


class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=TokenResponse,
        )
        self.router.add_api_route(
            "/me",
            self.me,
            methods=["GET"],
            response_model=UserInfo,
        )

    def login(self, body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
        user = authenticate_user(db, body.email, body.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
            )
        return TokenResponse(access_token=create_access_token(user.id))

    def me(self, current_user: User = Depends(get_current_user)) -> UserInfo:
        cartao = current_user.aluno.cartao_ufrgs if current_user.aluno else None
        return UserInfo(
            id=current_user.id,
            nome=current_user.nome,
            email=current_user.email,
            role=current_user.role,
            cartao_ufrgs=cartao,
        )
