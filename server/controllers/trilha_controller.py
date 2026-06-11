from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.trilha import TrilhaCreate, TrilhaResponse, TrilhaUpdate
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
        self.router.add_api_route(
            "/create",
            self.criar_trilha,
            methods=["POST"],
            response_model=TrilhaResponse,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/update/{trilha_id}",
            self.editar_trilha,
            methods=["PATCH"],
            response_model=TrilhaResponse,
        )
        self.router.add_api_route(
            "/delete/{trilha_id}",
            self.excluir_trilha,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

    def get_trilhas(
        self,
        disciplina: str | None = None,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.pesquisar(disciplina)

    def criar_trilha(
        self,
        payload: TrilhaCreate,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.cadastrar(
            nome=payload.nome,
            resumo=payload.resumo,
            disciplinas_ids=payload.disciplinas_ids,
        )

    def editar_trilha(
        self,
        trilha_id: int,
        payload: TrilhaUpdate,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        return service.editar(
            trilha_id,
            nome=payload.nome,
            resumo=payload.resumo,
            disciplinas_ids=payload.disciplinas_ids,
        )

    def excluir_trilha(
        self,
        trilha_id: int,
        db: Session = Depends(get_db),
    ):
        service = TrilhaService(db)
        service.excluir(trilha_id)
