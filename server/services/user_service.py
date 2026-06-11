from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.models.enums import UserRole
from server.models.user import User
from server.repositories.aluno_repository import AlunoRepository
from server.repositories.user_repository import UserRepository
from server.schemas.user import AlunoData
from server.services.auth_service import AuthService


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.aluno_repo = AlunoRepository(db)

    def listar(
        self,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        return self.user_repo.listar(role=role, is_active=is_active)

    def obter(self, user_id: int) -> User:
        user = self.user_repo.obter(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return user

    def cadastrar(
        self,
        *,
        email: str,
        nome: str,
        password: str,
        role: UserRole,
        aluno: AlunoData | None,
    ) -> User:
        if role == UserRole.ALUNO and aluno is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados de aluno são obrigatórios para role=ALUNO",
            )
        if role != UserRole.ALUNO and aluno is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados de aluno só são permitidos para role=ALUNO",
            )
        if self.user_repo.obter_por_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"E-mail '{email}' já está em uso",
            )

        password_hash = AuthService.hash_password(password)
        user = self.user_repo.criar(
            email=email, nome=nome, password_hash=password_hash, role=role
        )
        if aluno is not None:
            self.aluno_repo.criar(
                user_id=user.id,
                cartao_ufrgs=aluno.cartao_ufrgs,
                semestre_ingresso=aluno.semestre_ingresso,
            )
            self.db.refresh(user)
        return user

    def editar(
        self,
        user_id: int,
        *,
        email: str | None = None,
        nome: str | None = None,
        is_active: bool | None = None,
        aluno: AlunoData | None = None,
    ) -> User:
        user = self.user_repo.obter(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        if email is not None and email != user.email:
            outro = self.user_repo.obter_por_email(email)
            if outro is not None and outro.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"E-mail '{email}' já está em uso",
                )

        if aluno is not None and user.role != UserRole.ALUNO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados de aluno só podem ser editados para role=ALUNO",
            )

        self.user_repo.atualizar(
            user, email=email, nome=nome, is_active=is_active
        )

        if aluno is not None:
            existente = self.aluno_repo.obter_por_user_id(user.id)
            if existente is None:
                self.aluno_repo.criar(
                    user_id=user.id,
                    cartao_ufrgs=aluno.cartao_ufrgs,
                    semestre_ingresso=aluno.semestre_ingresso,
                )
            else:
                self.aluno_repo.atualizar(
                    existente,
                    cartao_ufrgs=aluno.cartao_ufrgs,
                    semestre_ingresso=aluno.semestre_ingresso,
                )
            self.db.refresh(user)

        return user

    def excluir(self, user_id: int) -> None:
        user = self.user_repo.obter(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        self.user_repo.soft_delete(user)
