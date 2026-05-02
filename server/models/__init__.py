from server.models.aluno import Aluno
from server.models.chamado import Chamado
from server.models.curriculo import Curriculo
from server.models.disciplina import Disciplina
from server.models.enums import (
    ChamadoStatus,
    ChamadoTipo,
    DisciplinaTipo,
    SolicitacaoStatus,
    UserRole,
)
from server.models.relatorio import Relatorio, RelatorioItem
from server.models.solicitacao import Solicitacao
from server.models.trilha import Trilha, trilha_disciplinas
from server.models.user import User

__all__ = [
    "Aluno",
    "Chamado",
    "ChamadoStatus",
    "ChamadoTipo",
    "Curriculo",
    "Disciplina",
    "DisciplinaTipo",
    "Relatorio",
    "RelatorioItem",
    "Solicitacao",
    "SolicitacaoStatus",
    "Trilha",
    "trilha_disciplinas",
    "User",
    "UserRole",
]
