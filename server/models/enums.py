import enum


class UserRole(str, enum.Enum):
    ALUNO = "ALUNO"
    COMGRAD = "COMGRAD"
    ADMIN = "ADMIN"


class DisciplinaTipo(str, enum.Enum):
    OBRIGATORIA = "OBRIGATORIA"
    ELETIVA = "ELETIVA"


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
