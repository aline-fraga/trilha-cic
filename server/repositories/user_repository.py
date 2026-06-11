from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models.enums import UserRole
from server.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter_por_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def obter(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def listar(
        self,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        stmt = select(User).options(selectinload(User.aluno))
        if role is not None:
            stmt = stmt.where(User.role == role)
        if is_active is not None:
            stmt = stmt.where(User.is_active.is_(is_active))
        stmt = stmt.order_by(User.created_at.desc())
        return list(self.db.scalars(stmt))

    def criar(
        self,
        *,
        email: str,
        nome: str,
        password_hash: str,
        role: UserRole,
    ) -> User:
        user = User(
            email=email, nome=nome, password_hash=password_hash, role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def atualizar(
        self,
        user: User,
        *,
        email: str | None = None,
        nome: str | None = None,
        is_active: bool | None = None,
    ) -> User:
        if email is not None:
            user.email = email
        if nome is not None:
            user.nome = nome
        if is_active is not None:
            user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)
        return user

    def soft_delete(self, user: User) -> None:
        user.is_active = False
        self.db.commit()
