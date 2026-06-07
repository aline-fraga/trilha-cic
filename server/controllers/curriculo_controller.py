from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.curriculo import CurriculoResponse
from server.services.curriculo_service import CurriculoService


class CurriculoController:
    def __init__(self):
        self.router = APIRouter(prefix="/curriculos", tags=["curriculos"])
        self.router.add_api_route(
            "/get",
            self.listar_curriculos,
            methods=["GET"],
            response_model=list[CurriculoResponse],
        )
        self.router.add_api_route(
            "/get/{curriculo_id}",
            self.obter_curriculo,
            methods=["GET"],
            response_model=CurriculoResponse,
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
