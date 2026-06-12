from server.models.aluno import Aluno
from server.models.chamado import Chamado
from server.models.curriculo import Curriculo, curriculo_disciplinas
from server.models.disciplina import Disciplina
from server.models.enums import (
    ChamadoStatus,
    ChamadoTipo,
    SolicitacaoStatus,
    UserRole,
)
from server.models.relatorio import Relatorio, RelatorioItem
from server.models.solicitacao import Solicitacao, solicitacao_trilhas_candidatas
from server.models.sugestao_trilha import SugestaoTrilha, sugestao_trilha_disciplinas
from server.models.trilha import Trilha, trilha_disciplinas
from server.models.user import User

__all__ = [
    "Aluno",
    "Chamado",
    "ChamadoStatus",
    "ChamadoTipo",
    "Curriculo",
    "curriculo_disciplinas",
    "Disciplina",
    "Relatorio",
    "RelatorioItem",
    "Solicitacao",
    "solicitacao_trilhas_candidatas",
    "SolicitacaoStatus",
    "SugestaoTrilha",
    "sugestao_trilha_disciplinas",
    "Trilha",
    "trilha_disciplinas",
    "User",
    "UserRole",
]
