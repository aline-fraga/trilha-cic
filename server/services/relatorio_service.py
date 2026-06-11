from datetime import datetime
from io import BytesIO

from fastapi import HTTPException, status
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.orm import Session

from server.models.enums import SolicitacaoStatus
from server.models.relatorio import Relatorio
from server.repositories.relatorio_repository import RelatorioRepository
from server.repositories.solicitacao_repository import SolicitacaoRepository
from server.repositories.trilha_repository import TrilhaRepository


class RelatorioService:
    def __init__(self, db: Session):
        self.relatorio_repo = RelatorioRepository(db)
        self.solicitacao_repo = SolicitacaoRepository(db)
        self.trilha_repo = TrilhaRepository(db)

    def listar(self) -> list[Relatorio]:
        return self.relatorio_repo.listar()

    def obter(self, relatorio_id: int) -> Relatorio:
        relatorio = self.relatorio_repo.obter(relatorio_id)
        if relatorio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relatório não encontrado",
            )
        return relatorio

    def gerar(
        self,
        *,
        gerado_por_id: int,
        periodo_inicio: datetime,
        periodo_fim: datetime,
    ) -> Relatorio:
        self._validar_periodo(periodo_inicio, periodo_fim)

        agregacao = self.solicitacao_repo.agregar_por_trilha(
            periodo_inicio, periodo_fim
        )
        contagens: dict[int, dict[SolicitacaoStatus, int]] = {}
        for trilha_id, status_, count in agregacao:
            contagens.setdefault(trilha_id, {})[status_] = count

        trilhas_ativas = self.trilha_repo.listar_ativas()
        itens: list[dict] = []
        total_aceites = 0
        total_rejeicoes = 0
        for trilha in trilhas_ativas:
            c = contagens.get(trilha.id, {})
            aceites = c.get(SolicitacaoStatus.ACEITA, 0)
            rejeicoes = c.get(SolicitacaoStatus.REJEITADA, 0)
            itens.append(
                {
                    "trilha_id": trilha.id,
                    "aceites": aceites,
                    "rejeicoes": rejeicoes,
                }
            )
            total_aceites += aceites
            total_rejeicoes += rejeicoes

        total_solicitacoes = total_aceites + total_rejeicoes

        return self.relatorio_repo.criar(
            gerado_por_id=gerado_por_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            total_solicitacoes=total_solicitacoes,
            total_aceites=total_aceites,
            total_rejeicoes=total_rejeicoes,
            itens=itens,
        )

    def _validar_periodo(
        self, periodo_inicio: datetime, periodo_fim: datetime
    ) -> None:
        inicio = self._naive(periodo_inicio)
        fim = self._naive(periodo_fim)
        if inicio >= fim:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="periodo_inicio deve ser anterior a periodo_fim",
            )
        if fim > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="periodo_fim deve estar no passado",
            )

    @staticmethod
    def _naive(dt: datetime) -> datetime:
        return dt.replace(tzinfo=None) if dt.tzinfo is not None else dt

    def gerar_pdf(self, relatorio_id: int) -> bytes:
        relatorio = self.obter(relatorio_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title="Relatório de Trilhas")
        styles = getSampleStyleSheet()

        elementos = [
            Paragraph("Relatório de Demanda de Trilhas", styles["Title"]),
            Spacer(1, 12),
            Paragraph(
                "Período: "
                f"{relatorio.periodo_inicio.strftime('%d/%m/%Y')} a "
                f"{relatorio.periodo_fim.strftime('%d/%m/%Y')}<br/>"
                f"Gerado em: {relatorio.created_at.strftime('%d/%m/%Y %H:%M')}<br/>"
                f"Total de solicitações: {relatorio.total_solicitacoes}<br/>"
                f"Total de aceites: {relatorio.total_aceites}<br/>"
                f"Total de rejeições: {relatorio.total_rejeicoes}",
                styles["Normal"],
            ),
            Spacer(1, 18),
        ]

        dados = [["Trilha", "Aceites", "Rejeições", "Total", "% Aceitação"]]
        for item in relatorio.itens:
            total_item = item.aceites + item.rejeicoes
            aceitacao = (
                f"{(item.aceites / total_item * 100):.1f}%"
                if total_item > 0
                else "—"
            )
            dados.append(
                [
                    item.trilha.nome,
                    item.aceites,
                    item.rejeicoes,
                    total_item,
                    aceitacao,
                ]
            )

        tabela = Table(dados, hAlign="LEFT")
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elementos.append(tabela)

        doc.build(elementos)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
