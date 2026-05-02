import re
import unicodedata

from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from server.models import Trilha
from server.repositories.disciplina_repository import DisciplinaRepository
from server.repositories.trilha_repository import TrilhaRepository


class TrilhaService:
    TOKEN_SCORE_CUTOFF = 65

    def __init__(self, db: Session):
        self.trilha_repo = TrilhaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)

    @staticmethod
    def _normalizar(s: str) -> str:
        nfd = unicodedata.normalize("NFD", s)
        sem_acento = "".join(c for c in nfd if not unicodedata.combining(c))
        return sem_acento.lower().strip()

    @staticmethod
    def _tokenizar(s: str) -> list[str]:
        return re.findall(r"\w+", s)

    def _casa(self, query_tokens: list[str], nome_tokens: list[str]) -> bool:
        if not query_tokens or not nome_tokens:
            return False
        return all(
            max(fuzz.ratio(qt, nt) for nt in nome_tokens) >= self.TOKEN_SCORE_CUTOFF
            for qt in query_tokens
        )

    def pesquisar(self, query: str | None) -> list[Trilha]:
        if query is None or not query.strip():
            return self.trilha_repo.listar_ativas()

        query_tokens = self._tokenizar(self._normalizar(query))
        if not query_tokens:
            return self.trilha_repo.listar_ativas()

        disciplinas = self.disciplina_repo.listar_ativas()
        ids_casados = [
            d.id
            for d in disciplinas
            if self._casa(query_tokens, self._tokenizar(self._normalizar(d.nome)))
        ]

        return self.trilha_repo.listar_por_disciplinas_ids(ids_casados)
