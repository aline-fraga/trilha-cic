from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrilhaBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str


class RelatorioCreate(BaseModel):
    periodo_inicio: datetime
    periodo_fim: datetime


class RelatorioItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trilha_id: int
    aceites: int
    rejeicoes: int
    trilha: TrilhaBrief


class RelatorioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    gerado_por_id: int
    periodo_inicio: datetime
    periodo_fim: datetime
    total_solicitacoes: int
    total_aceites: int
    total_rejeicoes: int
    created_at: datetime
    itens: list[RelatorioItemResponse]
