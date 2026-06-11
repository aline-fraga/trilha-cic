import os
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.models.user import User
from server.repositories.user_repository import UserRepository

SECRET_KEY = os.getenv("SECRET_KEY", "trilha-cic-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    @staticmethod
    def hash_password(plain: str) -> str:
        return pwd_context.hash(plain)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def criar_access_token(self, user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        return jwt.encode(
            {"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
        )

    def autenticar(self, email: str, password: str) -> User | None:
        user = self.user_repo.obter_por_email(email)
        if not user or not user.is_active:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

    def obter_usuario_atual(
        self, credentials: HTTPAuthorizationCredentials
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
            )
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.user_repo.obter(int(user_id))
        if user is None or not user.is_active:
            raise credentials_exception
        return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    return AuthService(db).obter_usuario_atual(credentials)


def require_roles(*roles: UserRole) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado",
            )
        return current_user

    return Depends(dependency)
