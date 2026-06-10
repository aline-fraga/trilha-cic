from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.models.user import User
from server.schemas.disciplina import DisciplinaCreate, DisciplinaResponse, DisciplinaUpdate
from server.services.auth_service import get_current_user, require_roles
from server.services.disciplina_service import DisciplinaService

_somente_comgrad = require_roles(UserRole.COMGRAD)
_comgrad_ou_admin = require_roles(UserRole.COMGRAD, UserRole.ADMIN)


class DisciplinaController:
    def __init__(self):
        self.router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])
        self.router.add_api_route(
            "",
            self.listar,
            methods=["GET"],
            response_model=list[DisciplinaResponse],
        )
        self.router.add_api_route(
            "/{disciplina_id}",
            self.buscar,
            methods=["GET"],
            response_model=DisciplinaResponse,
        )
        self.router.add_api_route(
            "",
            self.criar,
            methods=["POST"],
            response_model=DisciplinaResponse,
            status_code=201,
        )
        self.router.add_api_route(
            "/{disciplina_id}",
            self.atualizar,
            methods=["PUT"],
            response_model=DisciplinaResponse,
        )
        self.router.add_api_route(
            "/{disciplina_id}",
            self.excluir,
            methods=["DELETE"],
            status_code=204,
        )

    def listar(
        self,
        db: Session = Depends(get_db),
        _: User = _comgrad_ou_admin,
    ) -> list[DisciplinaResponse]:
        return DisciplinaService(db).listar()

    def buscar(
        self,
        disciplina_id: int,
        db: Session = Depends(get_db),
        _: User = _comgrad_ou_admin,
    ) -> DisciplinaResponse:
        return DisciplinaService(db).buscar(disciplina_id)

    def criar(
        self,
        body: DisciplinaCreate,
        db: Session = Depends(get_db),
        _: User = _somente_comgrad,
    ) -> DisciplinaResponse:
        disciplina = DisciplinaService(db).criar(body)
        db.commit()
        db.refresh(disciplina)
        return disciplina

    def atualizar(
        self,
        disciplina_id: int,
        body: DisciplinaUpdate,
        db: Session = Depends(get_db),
        _: User = _somente_comgrad,
    ) -> DisciplinaResponse:
        disciplina = DisciplinaService(db).atualizar(disciplina_id, body)
        db.commit()
        db.refresh(disciplina)
        return disciplina

    def excluir(
        self,
        disciplina_id: int,
        db: Session = Depends(get_db),
        _: User = _somente_comgrad,
    ) -> None:
        DisciplinaService(db).excluir(disciplina_id)
        db.commit()
