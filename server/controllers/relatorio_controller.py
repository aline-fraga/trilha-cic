from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.enums import UserRole
from server.models.user import User
from server.schemas.relatorio import RelatorioCreate, RelatorioResponse
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.services.auth_service import require_roles
from server.services.relatorio_service import RelatorioService


class RelatorioController:
    def __init__(self):
        self.router = APIRouter(prefix="/relatorios", tags=["relatorios"])
        comgrad_only = [require_roles(UserRole.COMGRAD)]
        comgrad_errors = {401: UNAUTHORIZED_401, 403: FORBIDDEN_403}

        self.router.add_api_route(
            "/get",
            self.listar_relatorios,
            methods=["GET"],
            response_model=list[RelatorioResponse],
            dependencies=comgrad_only,
            summary="Listar relatórios gerados (COMGRAD)",
            description=(
                "Lista todos os relatórios já gerados, ordenados por data de "
                "geração decrescente."
            ),
            responses={**comgrad_errors},
        )
        self.router.add_api_route(
            "/get/{relatorio_id}",
            self.obter_relatorio,
            methods=["GET"],
            response_model=RelatorioResponse,
            dependencies=comgrad_only,
            summary="Obter relatório por ID (COMGRAD)",
            description=(
                "Retorna os dados completos de um relatório, incluindo os itens "
                "por trilha (aceites e rejeições)."
            ),
            responses={**comgrad_errors, 404: NOT_FOUND_404},
        )
        self.router.add_api_route(
            "/create",
            self.gerar_relatorio,
            methods=["POST"],
            response_model=RelatorioResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Gerar novo relatório de demanda (COMGRAD)",
            description=(
                "Gera um snapshot do relatório de demanda de trilhas para um "
                "período fechado e persiste no banco. Conta apenas solicitações "
                "resolvidas (`ACEITA` ou `REJEITADA`) com `resolvido_em` dentro "
                "do intervalo — pendentes ficam de fora.\n\n"
                "**Regras:**\n"
                "- `periodo_inicio` deve ser anterior a `periodo_fim`.\n"
                "- `periodo_fim` deve estar no passado.\n"
                "- O autor (`gerado_por_id`) é capturado do token Bearer; não vai no body."
            ),
            responses={**comgrad_errors, 400: BAD_REQUEST_400},
        )
        self.router.add_api_route(
            "/get/{relatorio_id}/pdf",
            self.baixar_pdf,
            methods=["GET"],
            dependencies=comgrad_only,
            summary="Baixar relatório em PDF (COMGRAD)",
            description=(
                "Gera e retorna o PDF do relatório especificado. Resposta com "
                "`Content-Type: application/pdf` e `Content-Disposition: attachment`."
            ),
            responses={**comgrad_errors, 404: NOT_FOUND_404},
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
