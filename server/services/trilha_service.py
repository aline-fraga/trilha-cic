import unicodedata

from rapidfuzz import fuzz, process
from sqlalchemy.orm import Session

from server.models import Trilha
from server.repositories.disciplina_repository import DisciplinaRepository
from server.repositories.trilha_repository import TrilhaRepository


class TrilhaService:
    SCORE_CUTOFF = 80

    def __init__(self, db: Session):
        self.trilha_repo = TrilhaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)

    @staticmethod
    def _normalizar(s: str) -> str:
        nfd = unicodedata.normalize("NFD", s)
        sem_acento = "".join(c for c in nfd if not unicodedata.combining(c))
        return sem_acento.lower().strip()

    def pesquisar(self, query: str | None) -> list[Trilha]:
        if query is None or not query.strip():
            return self.trilha_repo.listar_ativas()

        disciplinas = self.disciplina_repo.listar_ativas()
        if not disciplinas:
            return []

        nomes_normalizados = {d.id: self._normalizar(d.nome) for d in disciplinas}
        query_normalizada = self._normalizar(query)

        matches = process.extract(
            query_normalizada,
            nomes_normalizados,
            scorer=fuzz.partial_ratio,
            score_cutoff=self.SCORE_CUTOFF,
            limit=None,
        )
        ids_casados = [match[2] for match in matches]

        return self.trilha_repo.listar_por_disciplinas_ids(ids_casados)
