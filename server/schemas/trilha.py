from pydantic import BaseModel, ConfigDict, Field

from server.schemas.disciplina import DisciplinaResumo


class TrilhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    resumo: str
    disciplinas: list[DisciplinaResumo]


class TrilhaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    resumo: str = Field(min_length=1)
    disciplinas_ids: list[int] = Field(min_length=1)


class TrilhaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=150)
    resumo: str | None = Field(default=None, min_length=1)
    disciplinas_ids: list[int] | None = Field(default=None, min_length=1)
