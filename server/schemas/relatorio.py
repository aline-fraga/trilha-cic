from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrilhaBrief(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "nome": "Ciência de Dados"}},
    )

    id: int
    nome: str


class RelatorioCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "periodo_inicio": "2026-04-01T00:00:00",
                "periodo_fim": "2026-06-10T23:59:59",
            }
        }
    )

    periodo_inicio: datetime
    periodo_fim: datetime


class RelatorioItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "trilha_id": 1,
                "aceites": 2,
                "rejeicoes": 1,
                "trilha": {"id": 1, "nome": "Ciência de Dados"},
            }
        },
    )

    trilha_id: int
    aceites: int
    rejeicoes: int
    trilha: TrilhaBrief


class RelatorioResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "gerado_por_id": 2,
                "periodo_inicio": "2026-04-01T00:00:00",
                "periodo_fim": "2026-06-10T23:59:59",
                "total_solicitacoes": 6,
                "total_aceites": 3,
                "total_rejeicoes": 3,
                "created_at": "2026-06-11T10:32:11",
                "itens": [
                    {
                        "trilha_id": 1,
                        "aceites": 2,
                        "rejeicoes": 1,
                        "trilha": {"id": 1, "nome": "Ciência de Dados"},
                    },
                    {
                        "trilha_id": 2,
                        "aceites": 1,
                        "rejeicoes": 2,
                        "trilha": {"id": 2, "nome": "Engenharia de Software"},
                    },
                ],
            }
        },
    )

    id: int
    gerado_por_id: int
    periodo_inicio: datetime
    periodo_fim: datetime
    total_solicitacoes: int
    total_aceites: int
    total_rejeicoes: int
    created_at: datetime
    itens: list[RelatorioItemResponse]
