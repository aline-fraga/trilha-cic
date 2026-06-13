from pydantic import BaseModel, ConfigDict, Field

from server.models.enums import PerguntaTipo


class PerguntaCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enunciado": "Tenho interesse em descobrir padrões ocultos em grandes volumes de dados.",
                "tipo": "CONCEITUAL",
                "ordem": 1,
            }
        }
    )

    enunciado: str = Field(min_length=1, max_length=500)
    tipo: PerguntaTipo
    ordem: int = Field(ge=0)


class PerguntaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "enunciado": "Tenho interesse em descobrir padrões ocultos em grandes massas de dados.",
                "ordem": 2,
            }
        }
    )

    enunciado: str | None = Field(default=None, min_length=1, max_length=500)
    tipo: PerguntaTipo | None = None
    ordem: int | None = Field(default=None, ge=0)


class PerguntaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "enunciado": "Tenho interesse em descobrir padrões ocultos em grandes volumes de dados.",
                "tipo": "CONCEITUAL",
                "ordem": 1,
                "is_active": True,
            }
        },
    )

    id: int
    enunciado: str
    tipo: PerguntaTipo
    ordem: int
    is_active: bool
