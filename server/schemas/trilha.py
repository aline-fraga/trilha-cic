from pydantic import BaseModel, ConfigDict, Field

from server.schemas.disciplina import DisciplinaResumo


class TrilhaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Ciência de Dados",
                "resumo": "Trilha focada em estatística, aprendizado de máquina e mineração de dados.",
                "disciplinas": [
                    {
                        "id": 12,
                        "nome": "Algoritmos e Estruturas de Dados",
                        "codigo": "INF01202",
                        "tipo": "OBRIGATORIA",
                        "carga_horaria": 60,
                        "link_plano_ensino": "https://www.inf.ufrgs.br/planos/inf01202.pdf",
                    }
                ],
            }
        },
    )

    id: int
    nome: str
    resumo: str
    disciplinas: list[DisciplinaResumo]


class TrilhaCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Inteligência Artificial",
                "resumo": "Trilha focada em IA, machine learning e processamento de linguagem natural.",
                "disciplinas_ids": [3, 7, 12, 18],
            }
        }
    )

    nome: str = Field(min_length=1, max_length=150)
    resumo: str = Field(min_length=1)
    disciplinas_ids: list[int] = Field(min_length=1, max_length=4)


class TrilhaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Inteligência Artificial Aplicada",
                "disciplinas_ids": [3, 7, 12, 18],
            }
        }
    )

    nome: str | None = Field(default=None, min_length=1, max_length=150)
    resumo: str | None = Field(default=None, min_length=1)
    disciplinas_ids: list[int] | None = Field(default=None, min_length=1, max_length=4)
