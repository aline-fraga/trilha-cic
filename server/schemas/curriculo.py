from pydantic import BaseModel, ConfigDict

from server.schemas.disciplina import DisciplinaResumo


class CurriculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    curso: str
    codigo: str
    ano_vigencia: int
    is_active: bool
    disciplinas: list[DisciplinaResumo]
