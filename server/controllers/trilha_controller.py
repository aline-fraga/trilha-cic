from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.trilha import TrilhaResponse
from server.services.trilha_service import TrilhaService


class TrilhaController:
    def __init__(self):
        self.router = APIRouter(prefix="/trilhas", tags=["trilhas"])
        self.router.add_api_route(
            "/get",
            self.get_trilhas,
            methods=["GET"],
            response_model=list[TrilhaResponse],
        )

    def get_trilhas(
        self,
        disciplina: str | None = None,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.pesquisar(disciplina)
