from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import server.models  # noqa: F401  -- registra todos os models em Base.metadata
from server.database import Base, get_db
from server.main import app
from server.models.enums import UserRole
from server.models.user import User
from server.services.auth_service import AuthService

collect_ignore = ["test_load.py"]

@pytest.fixture
def db_session() -> Iterator[Session]:
    """Sessão ligada a um banco SQLite in-memory recriado a cada teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    """TestClient com `get_db` apontando para a sessão de teste."""

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def criar_usuario(db_session: Session) -> Callable[..., User]:
    """Factory de usuários. Retorna o `User` persistido na sessão de teste."""
    contador = {"n": 0}

    def _criar(role: UserRole, nome: str | None = None) -> User:
        contador["n"] += 1
        n = contador["n"]
        user = User(
            email=f"user{n}@inf.ufrgs.br",
            password_hash=AuthService.hash_password("senha-teste"),
            nome=nome or f"Usuário {role.value} {n}",
            role=role,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _criar


@pytest.fixture
def auth_header(db_session: Session) -> Callable[[User], dict[str, str]]:
    """Gera o cabeçalho Bearer para um usuário já criado."""

    def _header(user: User) -> dict[str, str]:
        token = AuthService(db_session).criar_access_token(user.id)
        return {"Authorization": f"Bearer {token}"}

    return _header
