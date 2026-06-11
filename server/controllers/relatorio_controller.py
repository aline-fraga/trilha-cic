from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.models.user import User
from server.schemas.relatorio import RelatorioCreate, RelatorioResponse
from server.services.auth_service import require_roles
from server.services.relatorio_service import RelatorioService


class RelatorioController:
    def __init__(self):
        self.router = APIRouter(prefix="/relatorios", tags=["relatorios"])
        comgrad_only = [require_roles(UserRole.COMGRAD)]

        self.router.add_api_route(
            "/get",
            self.listar_relatorios,
            methods=["GET"],
            response_model=list[RelatorioResponse],
            dependencies=comgrad_only,
        )
        self.router.add_api_route(
            "/get/{relatorio_id}",
            self.obter_relatorio,
            methods=["GET"],
            response_model=RelatorioResponse,
            dependencies=comgrad_only,
        )
        self.router.add_api_route(
            "/create",
            self.gerar_relatorio,
            methods=["POST"],
            response_model=RelatorioResponse,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/get/{relatorio_id}/pdf",
            self.baixar_pdf,
            methods=["GET"],
            dependencies=comgrad_only,
        )

    def listar_relatorios(self, db: Session = Depends(get_db)):
        service = RelatorioService(db)
        return service.listar()

    def obter_relatorio(
        self,
        relatorio_id: int,
        db: Session = Depends(get_db),
    ):
        service = RelatorioService(db)
        return service.obter(relatorio_id)

    def gerar_relatorio(
        self,
        payload: RelatorioCreate,
        current_user: User = require_roles(UserRole.COMGRAD),
        db: Session = Depends(get_db),
    ):
        service = RelatorioService(db)
        return service.gerar(
            gerado_por_id=current_user.id,
            periodo_inicio=payload.periodo_inicio,
            periodo_fim=payload.periodo_fim,
        )

    def baixar_pdf(
        self,
        relatorio_id: int,
        db: Session = Depends(get_db),
    ):
        service = RelatorioService(db)
        pdf_bytes = service.gerar_pdf(relatorio_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="relatorio_{relatorio_id}.pdf"'
                )
            },
        )
