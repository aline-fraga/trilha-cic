from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models.relatorio import Relatorio, RelatorioItem


class RelatorioRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Relatorio]:
        stmt = (
            select(Relatorio)
            .options(
                selectinload(Relatorio.itens).selectinload(RelatorioItem.trilha)
            )
            .order_by(Relatorio.created_at.desc())
        )
        return list(self.db.scalars(stmt))

    def obter(self, relatorio_id: int) -> Relatorio | None:
        stmt = (
            select(Relatorio)
            .where(Relatorio.id == relatorio_id)
            .options(
                selectinload(Relatorio.itens).selectinload(RelatorioItem.trilha)
            )
        )
        return self.db.scalars(stmt).one_or_none()

    def criar(
        self,
        *,
        gerado_por_id: int,
        periodo_inicio: datetime,
        periodo_fim: datetime,
        total_solicitacoes: int,
        total_aceites: int,
        total_rejeicoes: int,
        itens: list[dict],
    ) -> Relatorio:
        relatorio = Relatorio(
            gerado_por_id=gerado_por_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            total_solicitacoes=total_solicitacoes,
            total_aceites=total_aceites,
            total_rejeicoes=total_rejeicoes,
            itens=[RelatorioItem(**item) for item in itens],
        )
        self.db.add(relatorio)
        self.db.commit()
        self.db.refresh(relatorio)
        return relatorio
