from datetime import datetime

from pydantic import BaseModel, ConfigDict

from server.models.enums import SolicitacaoStatus
from server.schemas.chamado import ChamadoResponse
from server.schemas.trilha import TrilhaResponse


class AceitarTrilhaRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"trilha_id": 2}}
    )

    trilha_id: int


class SolicitacaoResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 4,
                "aluno_id": 3,
                "aluno_nome": "Aline Fraga",
                "trilhas_candidatas": [
                    {
                        "id": 2,
                        "nome": "Ciência de Dados",
                        "resumo": "Trilha voltada à análise e ciência de dados.",
                        "disciplinas": [],
                    },
                    {
                        "id": 5,
                        "nome": "Engenharia de Software",
                        "resumo": "Trilha de ES.",
                        "disciplinas": [],
                    },
                ],
                "trilha_aceita": None,
                "chamado": None,
                "status": "PENDENTE",
                "created_at": "2026-06-12T15:30:00",
                "resolvido_em": None,
            }
        },
    )

    id: int
    aluno_id: int
    aluno_nome: str
    trilhas_candidatas: list[TrilhaResponse]
    trilha_aceita: TrilhaResponse | None = None
    chamado: ChamadoResponse | None = None
    status: SolicitacaoStatus
    created_at: datetime
    resolvido_em: datetime | None = None
