import enum


class UserRole(str, enum.Enum):
    ALUNO = "ALUNO"
    COMGRAD = "COMGRAD"
    ADMIN = "ADMIN"


class ChamadoTipo(str, enum.Enum):
    TRILHA_REJEITADA = "TRILHA_REJEITADA"
    NOVA_TRILHA = "NOVA_TRILHA"


class ChamadoStatus(str, enum.Enum):
    ABERTO = "ABERTO"
    FECHADO = "FECHADO"


class SolicitacaoStatus(str, enum.Enum):
    PENDENTE = "PENDENTE"
    ACEITA = "ACEITA"
    REJEITADA = "REJEITADA"


class PerguntaTipo(str, enum.Enum):
    CONCEITUAL = "CONCEITUAL"
    PRATICA = "PRATICA"


class DisciplinaTipo(str, enum.Enum):
    OBRIGATORIA = "OBRIGATORIA"
    ELETIVA = "ELETIVA"
