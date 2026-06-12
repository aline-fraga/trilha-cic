from fastapi import HTTPException
from sqlalchemy.orm import Session

from server.models import Disciplina, SugestaoTrilha
from server.models.enums import ChamadoTipo
from server.repositories.disciplina_repository import DisciplinaRepository
from server.repositories.sugestao_trilha_repository import SugestaoTrilhaRepository
from server.schemas.chamado import ChamadoCreate
from server.services.chamado_service import ChamadoService


class SugestaoTrilhaService:
    def __init__(self, db: Session):
        self.sugestao_repo = SugestaoTrilhaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)
        self.chamado_service = ChamadoService(db)

    def sugerir(
        self, aluno_id: int, nome: str, disciplinas_ids: list[int]
    ) -> SugestaoTrilha:
        nome_normalizado = nome.strip()
        if not nome_normalizado:
            raise HTTPException(
                status_code=400, detail="O nome da trilha não pode estar em branco."
            )

        disciplinas = self._resolver_disciplinas(disciplinas_ids)
        chamado = self.chamado_service.criar(
            ChamadoCreate(
                tipo=ChamadoTipo.NOVA_TRILHA,
                assunto=f"Nova trilha: {nome_normalizado}",
                mensagem=self._montar_mensagem(nome_normalizado, disciplinas),
            ),
            aluno_id,
        )
        return self.sugestao_repo.criar(
            aluno_id=aluno_id,
            chamado_id=chamado.id,
            nome_proposto=nome_normalizado,
            disciplinas=disciplinas,
        )

    def listar(self, aluno_id: int | None = None) -> list[SugestaoTrilha]:
        return self.sugestao_repo.listar(aluno_id=aluno_id)

    def obter(self, sugestao_id: int) -> SugestaoTrilha:
        sugestao = self.sugestao_repo.obter(sugestao_id)
        if sugestao is None:
            raise HTTPException(
                status_code=404, detail="Sugestão de trilha não encontrada."
            )
        return sugestao

    def _resolver_disciplinas(self, ids: list[int]) -> list[Disciplina]:
        unicos = list(dict.fromkeys(ids))
        disciplinas = self.disciplina_repo.listar_por_ids_ativas(unicos)
        if len(disciplinas) != len(unicos):
            encontrados = {d.id for d in disciplinas}
            invalidos = [i for i in unicos if i not in encontrados]
            raise HTTPException(
                status_code=400,
                detail=f"Disciplinas inválidas ou inativas: {invalidos}",
            )
        return disciplinas

    @staticmethod
    def _montar_mensagem(nome: str, disciplinas: list[Disciplina]) -> str:
        nomes = ", ".join(d.nome for d in disciplinas)
        return (
            f"Sugestão de nova trilha proposta pelo aluno: '{nome}'. "
            f"Disciplinas selecionadas ({len(disciplinas)}): {nomes}."
        )
