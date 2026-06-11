from datetime import datetime
from pydantic import BaseModel, ConfigDict

from server.models.enums import ChamadoTipo, ChamadoStatus


class ChamadoCreate(BaseModel):
    assunto: str
    mensagem: str
    tipo: ChamadoTipo

class ChamadoResponder(BaseModel):
    resposta: str

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

