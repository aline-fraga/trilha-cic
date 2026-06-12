from pydantic import BaseModel, ConfigDict, field_validator


class DisciplinaCreate(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int

    @field_validator("nome", "codigo")
    @classmethod
    def nao_vazio(cls, v: str, info) -> str:
        if not v or not v.strip():
            raise ValueError(f"O campo '{info.field_name}' não pode ser vazio")
        return v.strip()

    @field_validator("carga_horaria")
    @classmethod
    def carga_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("carga_horaria deve ser maior que zero")
        return v


class DisciplinaUpdate(BaseModel):
    nome: str | None = None
    codigo: str | None = None
    carga_horaria: int | None = None

    @field_validator("nome", "codigo")
    @classmethod
    def nao_vazio(cls, v: str | None, info) -> str | None:
        if v is not None and not v.strip():
            raise ValueError(f"O campo '{info.field_name}' não pode ser vazio")
        return v.strip() if v else v

    @field_validator("carga_horaria")
    @classmethod
    def carga_positiva(cls, v: int | None) -> int | None:
        if v is not None and v <= 0:
            raise ValueError("carga_horaria deve ser maior que zero")
        return v


class DisciplinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    codigo: str
    carga_horaria: int
    is_active: bool


class DisciplinaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    codigo: str
    carga_horaria: int
