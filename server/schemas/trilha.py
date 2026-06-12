from pydantic import BaseModel, ConfigDict


class DisciplinaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    codigo: str
    carga_horaria: int


class TrilhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    resumo: str
    disciplinas: list[DisciplinaResumo]
