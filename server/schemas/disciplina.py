from pydantic import BaseModel, ConfigDict

from server.models.enums import DisciplinaTipo


class DisciplinaResumo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 12,
                "nome": "Algoritmos e Estruturas de Dados",
                "codigo": "INF01202",
                "tipo": "OBRIGATORIA",
                "carga_horaria": 60,
                "link_plano_ensino": "https://www.inf.ufrgs.br/planos/inf01202.pdf",
            }
        },
    )

    id: int
    nome: str
    codigo: str
    tipo: DisciplinaTipo
    carga_horaria: int
    link_plano_ensino: str | None = None
