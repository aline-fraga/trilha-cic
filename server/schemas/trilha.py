from pydantic import BaseModel, ConfigDict

from server.models.enums import DisciplinaTipo


class DisciplinaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    codigo: str
    tipo: DisciplinaTipo
    carga_horaria: int
    link_plano_ensino: str | None = None


class TrilhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    resumo: str
    disciplinas: list[DisciplinaResumo]
