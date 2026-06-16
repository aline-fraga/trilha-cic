from datetime import datetime
from io import BytesIO

from fastapi import HTTPException
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.orm import Session

from server.models.enums import ChamadoTipo, SolicitacaoStatus
from server.models.solicitacao import Solicitacao
from server.repositories.solicitacao_repository import SolicitacaoRepository
from server.schemas.chamado import ChamadoCreate
from server.schemas.solicitacao import RespostaPerguntaInput
from server.services.chamado_service import ChamadoService
from server.services.trilha_service import TrilhaService
from server.services.user_service import UserService


class SolicitacaoService:
    def __init__(self, db: Session):
        self.db = db
        self.solicitacao_repo = SolicitacaoRepository(db)
        self.chamado_service = ChamadoService(db)
        self.trilha_service = TrilhaService(db)

    def listar(
        self,
        aluno_id: int | None = None,
        status: SolicitacaoStatus | None = None,
    ) -> list[Solicitacao]:
        return self.solicitacao_repo.listar(aluno_id=aluno_id, status=status)

    def obter(self, solicitacao_id: int) -> Solicitacao:
        solicitacao = self.solicitacao_repo.obter(solicitacao_id)
        if solicitacao is None:
            raise HTTPException(
                status_code=404, detail="Solicitação não encontrada."
            )
        return solicitacao

    def solicitar(
        self, aluno_id: int, respostas: list[RespostaPerguntaInput]
    ) -> Solicitacao:
        if self.chamado_service.existe_aberto_para_aluno(aluno_id):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Aluno já possui um chamado em aberto. "
                    "Aguarde a resposta da COMGRAD antes de solicitar nova trilha."
                ),
            )
        if self.solicitacao_repo.existe_pendente_para_aluno(aluno_id):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Aluno já possui uma solicitação pendente. "
                    "Aceite ou rejeite a atual antes de solicitar nova."
                ),
            )
        if self.solicitacao_repo.existe_aceita_para_aluno(aluno_id):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Aluno já possui uma trilha aceita. "
                    "Apenas uma trilha aceita por aluno é permitida."
                ),
            )

        trilhas_candidatas = self.trilha_service.sugerir_trilhas(respostas)
        solicitacao = self.solicitacao_repo.criar(
            aluno_id=aluno_id, trilhas_candidatas=trilhas_candidatas
        )
        return self.obter(solicitacao.id)

    def aceitar(
        self, solicitacao_id: int, aluno_id: int, trilha_id: int
    ) -> Solicitacao:
        solicitacao = self.obter(solicitacao_id)

        if solicitacao.aluno_id != aluno_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        if solicitacao.status != SolicitacaoStatus.PENDENTE:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Solicitação já resolvida — status atual: "
                    f"{solicitacao.status.value}."
                ),
            )

        if self.solicitacao_repo.existe_aceita_para_aluno(aluno_id):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Aluno já possui uma trilha aceita. "
                    "Apenas uma trilha aceita por aluno é permitida."
                ),
            )

        trilha_escolhida = next(
            (t for t in solicitacao.trilhas_candidatas if t.id == trilha_id),
            None,
        )
        if trilha_escolhida is None:
            ids_validos = [t.id for t in solicitacao.trilhas_candidatas]
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Trilha {trilha_id} não está entre as candidatas desta "
                    f"solicitação. Candidatas válidas: {ids_validos}."
                ),
            )

        return self.solicitacao_repo.aceitar(solicitacao, trilha_escolhida)

    def rejeitar(self, solicitacao_id: int, aluno_id: int) -> Solicitacao:
        solicitacao = self.obter(solicitacao_id)

        if solicitacao.aluno_id != aluno_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        if solicitacao.status != SolicitacaoStatus.PENDENTE:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Solicitação já resolvida — status atual: "
                    f"{solicitacao.status.value}."
                ),
            )

        chamado = self.chamado_service.criar(
            ChamadoCreate(
                tipo=ChamadoTipo.TRILHA_REJEITADA,
                assunto=f"Trilhas sugeridas rejeitadas — solicitação #{solicitacao.id}",
                mensagem=self._montar_mensagem_rejeicao(solicitacao),
            ),
            aluno_id,
        )
        return self.solicitacao_repo.rejeitar(solicitacao, chamado.id)

    @staticmethod
    def _montar_mensagem_rejeicao(solicitacao: Solicitacao) -> str:
        nomes = ", ".join(t.nome for t in solicitacao.trilhas_candidatas)
        return (
            f"O aluno rejeitou as trilhas sugeridas: {nomes}. "
            f"Solicitação #{solicitacao.id}. "
            "Aguardando orientação personalizada da COMGRAD."
        )

    def gerar_material_pdf(
        self, solicitacao_id: int, aluno_id: int
    ) -> bytes:
        solicitacao = self.obter(solicitacao_id)

        if solicitacao.aluno_id != aluno_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        if solicitacao.status != SolicitacaoStatus.ACEITA:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Material disponível apenas para solicitações com trilha "
                    f"aceita — status atual: {solicitacao.status.value}."
                ),
            )

        trilha = solicitacao.trilha_aceita
        if trilha is None:
            raise HTTPException(
                status_code=400,
                detail="Solicitação aceita sem trilha vinculada.",
            )

        aluno = UserService(self.db).obter(aluno_id)
        nome_aluno = aluno.nome if aluno else "Desconhecido"

        return self._montar_pdf_material(
            trilha=trilha,
            nome_aluno=nome_aluno,
            aceito_em=solicitacao.resolvido_em,
        )

    @staticmethod
    def _montar_pdf_material(
        trilha, nome_aluno: str, aceito_em: datetime | None
    ) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4, title=f"Material da Trilha — {trilha.nome}"
        )
        styles = getSampleStyleSheet()

        data_aceite = (
            aceito_em.strftime("%d/%m/%Y") if aceito_em is not None else "—"
        )

        elementos = [
            Paragraph(f"Material da Trilha: {trilha.nome}", styles["Title"]),
            Spacer(1, 6),
            Paragraph(
                f"<b>Aluno:</b> {nome_aluno} &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"<b>Aceito em:</b> {data_aceite}",
                styles["Normal"],
            ),
            Spacer(1, 12),
            Paragraph(trilha.resumo, styles["Normal"]),
            Spacer(1, 18),
            Paragraph("Disciplinas da trilha", styles["Heading2"]),
            Spacer(1, 6),
        ]

        dados = [["Código", "Nome", "Tipo", "Carga horária", "Plano de ensino"]]
        total_horas = 0
        for disciplina in trilha.disciplinas:
            total_horas += disciplina.carga_horaria
            dados.append(
                [
                    disciplina.codigo,
                    disciplina.nome,
                    disciplina.tipo.value,
                    f"{disciplina.carga_horaria}h",
                    disciplina.link_plano_ensino or "—",
                ]
            )

        tabela = Table(dados, hAlign="LEFT")
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        elementos.append(tabela)
        elementos.append(Spacer(1, 12))
        elementos.append(
            Paragraph(
                f"<b>Carga horária total:</b> {total_horas}h",
                styles["Normal"],
            )
        )

        def desenhar_rodape(canvas, doc_):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(
                A4[0] / 2.0,
                1 * cm,
                f"TrilhaCiC — UFRGS/INF — Página {doc_.page}",
            )
            canvas.restoreState()

        doc.build(
            elementos,
            onFirstPage=desenhar_rodape,
            onLaterPages=desenhar_rodape,
        )
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
