from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.curriculo import CurriculoResponse
from server.schemas.responses import NOT_FOUND_404
from server.services.curriculo_service import CurriculoService


class CurriculoController:
    def __init__(self):
        self.router = APIRouter(prefix="/curriculos", tags=["curriculos"])
        self.router.add_api_route(
            "/get",
            self.listar_curriculos,
            methods=["GET"],
            response_model=list[CurriculoResponse],
            summary="Listar currículos",
            description=(
                "Lista os currículos cadastrados, ordenados por ano de vigência "
                "decrescente. Aceita filtro opcional `is_active` "
                "(`true`/`false`). Sem o filtro, retorna ativos e inativos."
            ),
        )
        self.router.add_api_route(
            "/get/{curriculo_id}",
            self.obter_curriculo,
            methods=["GET"],
            response_model=CurriculoResponse,
            summary="Obter currículo por ID",
            description=(
                "Retorna os dados completos de um currículo, incluindo a lista "
                "de disciplinas associadas."
            ),
            responses={404: NOT_FOUND_404},
        )

    def listar_curriculos(
        self,
        is_active: bool | None = None,
        db: Session = Depends(get_db),
    ):
        service = CurriculoService(db)
        return service.listar(is_active=is_active)

    def obter_curriculo(
        self,
        curriculo_id: int,
        db: Session = Depends(get_db),
    ):
        service = CurriculoService(db)
        curriculo = service.obter(curriculo_id)
        if curriculo is None:
            raise HTTPException(status_code=404, detail="Currículo não encontrado")
        return curriculo
