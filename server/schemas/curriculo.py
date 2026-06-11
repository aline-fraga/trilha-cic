from pydantic import BaseModel, ConfigDict

from server.schemas.disciplina import DisciplinaResumo


class CurriculoResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "curso": "Ciência da Computação",
                "codigo": "CIC-2024",
                "ano_vigencia": 2024,
                "is_active": True,
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
    curso: str
    codigo: str
    ano_vigencia: int
    is_active: bool
    disciplinas: list[DisciplinaResumo]
