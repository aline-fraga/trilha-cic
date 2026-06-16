from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from server.models.enums import ChamadoTipo, ChamadoStatus

# RNF #12 (UC07): o comentário do aluno deve ter entre 50 e 2000 caracteres.
COMENTARIO_MIN_CHARS = 50
COMENTARIO_MAX_CHARS = 2000


class ChamadoCreate(BaseModel):
    # DTO interno/compartilhado — usado também pelos chamados gerados
    # automaticamente (UC06/UC13). Por isso NÃO carrega o limite de caracteres
    # do RNF #12, que vale apenas para o comentário digitado pelo aluno.
    assunto: str
    mensagem: str
    tipo: ChamadoTipo


class AbrirChamadoRequest(BaseModel):
    """Corpo do `POST /chamados` (UC07) — comentário digitado pelo aluno.

    Aplica o RNF #12 (50 a 2000 caracteres) sem acoplar os fluxos internos.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "assunto": "Revisão de Trilha Sugerida",
                "mensagem": (
                    "Rejeitei a trilha sugerida porque já cursei metade das "
                    "disciplinas e gostaria de orientação personalizada."
                ),
                "tipo": "TRILHA_REJEITADA",
            }
        }
    )

    assunto: str
    tipo: ChamadoTipo
    mensagem: str = Field(
        min_length=COMENTARIO_MIN_CHARS, max_length=COMENTARIO_MAX_CHARS
    )

class ChamadoResponder(BaseModel):
    resposta: str


class ChamadoEditMensagem(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "mensagem": (
                    "Atualização: já cursei três das disciplinas listadas e "
                    "preciso revisar minha trilha com base nisso."
                )
            }
        }
    )

    mensagem: str = Field(
        min_length=COMENTARIO_MIN_CHARS, max_length=COMENTARIO_MAX_CHARS
    )

class ChamadoResponse(ChamadoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    aluno_id: int
    aluno_nome: str | None = None
    status: ChamadoStatus
    created_at: datetime
    updated_at: datetime

    resposta: str | None = None
    respondido_em: datetime | None = None
    trilha_id: int | None = None

