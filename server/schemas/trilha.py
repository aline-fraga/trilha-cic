from pydantic import BaseModel, ConfigDict, Field

from server.schemas.disciplina import DisciplinaResumo


class PesoPerguntaInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"pergunta_id": 1, "peso": 1.0}}
    )

    pergunta_id: int
    peso: float = Field(ge=0.0, le=1.0)


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
                "pesos": [
                    {"pergunta_id": 1, "peso": 0.2},
                    {"pergunta_id": 2, "peso": 1.0},
                    {"pergunta_id": 3, "peso": 0.4},
                ],
            }
        }
    )

    nome: str = Field(min_length=1, max_length=150)
    resumo: str = Field(min_length=1)
    disciplinas_ids: list[int] = Field(min_length=1)
    pesos: list[PesoPerguntaInput] = Field(
        min_length=1,
        description=(
            "Pesos da trilha em cada pergunta ativa do sistema. Precisa cobrir "
            "todas as perguntas ativas; pesos omitidos disparam erro 400. Use "
            "`peso=0` para sinalizar que a pergunta não pontua nesta trilha."
        ),
    )


class TrilhaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Inteligência Artificial Aplicada",
                "disciplinas_ids": [3, 7, 12, 18, 22],
                "pesos": [
                    {"pergunta_id": 1, "peso": 0.2},
                    {"pergunta_id": 2, "peso": 1.0},
                    {"pergunta_id": 3, "peso": 0.4},
                ],
            }
        }
    )

    nome: str | None = Field(default=None, min_length=1, max_length=150)
    resumo: str | None = Field(default=None, min_length=1)
    disciplinas_ids: list[int] | None = Field(default=None, min_length=1)
    pesos: list[PesoPerguntaInput] | None = Field(
        default=None,
        description=(
            "Se enviado, **substitui** completamente os pesos da trilha. "
            "Precisa cobrir todas as perguntas ativas (use `peso=0` se a "
            "pergunta não pontua na trilha). Se omitido, os pesos atuais ficam."
        ),
    )
