from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from server.schemas.chamado import ChamadoResponse
from server.schemas.disciplina import DisciplinaResumo


class SugestaoTrilhaCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Computação Quântica Aplicada",
                "disciplinas_ids": [12, 27, 41],
            }
        }
    )

    nome: str = Field(min_length=1, max_length=150)
    disciplinas_ids: list[int] = Field(min_length=1, max_length=4)


class SugestaoTrilhaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 7,
                "nome_proposto": "Computação Quântica Aplicada",
                "aluno_id": 3,
                "aluno_nome": "Aline Fraga",
                "chamado": {
                    "id": 15,
                    "aluno_id": 3,
                    "aluno_nome": "Aline Fraga",
                    "tipo": "NOVA_TRILHA",
                    "assunto": "Nova trilha: Computação Quântica Aplicada",
                    "mensagem": (
                        "Sugestão de nova trilha proposta pelo aluno: "
                        "'Computação Quântica Aplicada'. Disciplinas "
                        "selecionadas (1): Algoritmos e Estruturas de Dados."
                    ),
                    "status": "ABERTO",
                    "resposta": None,
                    "respondido_em": None,
                    "trilha_id": None,
                    "created_at": "2026-06-12T15:30:00",
                    "updated_at": "2026-06-12T15:30:00",
                },
                "disciplinas": [
                    {
                        "id": 12,
                        "nome": "Algoritmos e Estruturas de Dados",
                        "codigo": "INF01202",
                        "tipo": "OBRIGATORIA",
                        "carga_horaria": 60,
                        "link_plano_ensino": None,
                    }
                ],
                "created_at": "2026-06-12T15:30:00",
            }
        },
    )

    id: int
    nome_proposto: str
    aluno_id: int
    aluno_nome: str
    chamado: ChamadoResponse
    disciplinas: list[DisciplinaResumo]
    created_at: datetime
