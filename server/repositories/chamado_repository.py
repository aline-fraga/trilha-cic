from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import Chamado
from server.models.enums import ChamadoStatus, ChamadoTipo

MOCK_CHAMADOS = [
    Chamado(
        id=1,
        aluno_id=1,
        tipo=ChamadoTipo.TRILHA_REJEITADA,
        assunto="Dúvida sobre rejeição de trilha",
        mensagem="Minha trilha de 'Desenvolvimento Web' foi rejeitada. Gostaria de saber os motivos detalhados.",
        status=ChamadoStatus.ABERTO,
        created_at=datetime.now(timezone.utc) - timedelta(days=2),
        updated_at=datetime.now(timezone.utc) - timedelta(days=2),
    ),
    Chamado(
        id=2,
        aluno_id=1,
        tipo=ChamadoTipo.NOVA_TRILHA,
        assunto="Problema no cadastro de nova trilha",
        mensagem="Ao tentar submeter a trilha de 'Data Science', o sistema não salva as disciplinas.",
        status=ChamadoStatus.FECHADO,
        resposta="Problema de banco de dados corrigido. Pode submeter novamente.",
        respondido_por_id=2,
        respondido_em=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc) - timedelta(days=5),
        updated_at=datetime.now(timezone.utc) - timedelta(days=1),
    ),
    Chamado(
        id=3,
        aluno_id=1,
        tipo=ChamadoTipo.NOVA_TRILHA,
        assunto="Sugestão de Trilhas baseadas em IA",
        mensagem="Gostaria de propor que a comgrad avaliasse adicionar trilhas de Inteligência Artificial pré-aprovadas.",
        status=ChamadoStatus.ABERTO,
        created_at=datetime.now(timezone.utc) - timedelta(days=10),
        updated_at=datetime.now(timezone.utc) - timedelta(days=10),
    )
]

MOCK_ID_COUNTER = 4

class ChamadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, chamado: Chamado) -> Chamado:
        # REMOVER COMENTARIO APOS TESTES
        # self.db.add(chamado)
        # self.db.commit()
        # self.db.refresh(chamado)
        # return chamado
        
        # MOCK CODIGO
        global MOCK_ID_COUNTER
        if getattr(chamado, "id", None) is None:
            chamado.id = MOCK_ID_COUNTER
            MOCK_ID_COUNTER += 1
            if getattr(chamado, "created_at", None) is None:
                chamado.created_at = datetime.now(timezone.utc)
            if getattr(chamado, "updated_at", None) is None:
                chamado.updated_at = datetime.now(timezone.utc)
            if getattr(chamado, "status", None) is None:
                chamado.status = ChamadoStatus.ABERTO
            MOCK_CHAMADOS.append(chamado)
        else:
            chamado.updated_at = datetime.now(timezone.utc)
            for i, c in enumerate(MOCK_CHAMADOS):
                if c.id == chamado.id:
                    MOCK_CHAMADOS[i] = chamado
                    break
        return chamado

    def listar(self, status: str | None = None) -> list[Chamado]:
        # REMOVER COMENTARIO APOS TESTES
        # stmt = select(Chamado)
        # if status is not None:
        #     stmt = stmt.where(Chamado.status == status)
        # stmt = stmt.order_by(Chamado.created_at.desc())
        # return list(self.db.scalars(stmt))
        
        # MOCK CODIGO
        res = MOCK_CHAMADOS
        if status:
            res = [c for c in res if (c.status.value == status if hasattr(c.status, "value") else c.status == status)]
        return sorted(res, key=lambda c: c.created_at, reverse=True)

    def buscar(self, chamado_id: int) -> Chamado | None:
        # REMOVER COMENTARIO APOS TESTES
        # stmt = select(Chamado).where(Chamado.id == chamado_id)
        # return self.db.scalars(stmt).one_or_none()
        
        # MOCK CODIGO
        for c in MOCK_CHAMADOS:
            if c.id == chamado_id:
                return c
        return None
