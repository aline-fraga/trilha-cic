import re
import unicodedata

from fastapi import HTTPException
from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from server.models import Disciplina, Trilha
from server.repositories.disciplina_repository import DisciplinaRepository
from server.repositories.pergunta_repository import PerguntaRepository
from server.repositories.trilha_repository import TrilhaRepository
from server.schemas.solicitacao import RespostaPerguntaInput
from server.schemas.trilha import PesoPerguntaInput


class TrilhaService:
    TOKEN_SCORE_CUTOFF = 65
    GAP_PERFIL_DECIDIDO = 0.20
    GAP_PERFIL_DEFINIDO = 0.10
    N_MIN_CANDIDATAS = 2
    N_MAX_CANDIDATAS = 4

    def __init__(self, db: Session):
        self.trilha_repo = TrilhaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)
        self.pergunta_repo = PerguntaRepository(db)

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

    def cadastrar(
        self,
        nome: str,
        resumo: str,
        disciplinas_ids: list[int],
        pesos: list[PesoPerguntaInput],
    ) -> Trilha:
        disciplinas = self._resolver_disciplinas(disciplinas_ids)
        pesos_validados = self._validar_pesos(pesos)
        return self.trilha_repo.criar(
            nome=nome,
            resumo=resumo,
            disciplinas=disciplinas,
            pesos=pesos_validados,
        )

    def editar(
        self,
        trilha_id: int,
        nome: str | None = None,
        resumo: str | None = None,
        disciplinas_ids: list[int] | None = None,
        pesos: list[PesoPerguntaInput] | None = None,
    ) -> Trilha:
        trilha = self.trilha_repo.obter(trilha_id)
        if trilha is None:
            raise HTTPException(status_code=404, detail="Trilha não encontrada")
        disciplinas = (
            self._resolver_disciplinas(disciplinas_ids)
            if disciplinas_ids is not None
            else None
        )
        pesos_validados = self._validar_pesos(pesos) if pesos is not None else None
        return self.trilha_repo.atualizar(
            trilha,
            nome=nome,
            resumo=resumo,
            disciplinas=disciplinas,
            pesos=pesos_validados,
        )

    def excluir(self, trilha_id: int) -> None:
        trilha = self.trilha_repo.obter(trilha_id)
        if trilha is None:
            raise HTTPException(status_code=404, detail="Trilha não encontrada")
        self.trilha_repo.soft_delete(trilha)

    def sugerir_trilhas(
        self, respostas: list[RespostaPerguntaInput]
    ) -> list[Trilha]:
        perguntas = self.pergunta_repo.listar_ativas()
        if not perguntas:
            raise HTTPException(
                status_code=400,
                detail="Não há perguntas ativas cadastradas no sistema.",
            )

        ids_perguntas = {p.id for p in perguntas}
        respostas_map: dict[int, int] = {}
        for r in respostas:
            if r.pergunta_id in respostas_map:
                raise HTTPException(
                    status_code=400,
                    detail=f"Pergunta {r.pergunta_id} respondida mais de uma vez.",
                )
            respostas_map[r.pergunta_id] = r.valor

        faltando = ids_perguntas - respostas_map.keys()
        sobrando = respostas_map.keys() - ids_perguntas
        if faltando or sobrando:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Respostas não correspondem às perguntas ativas. "
                    f"Faltando: {sorted(faltando)}; "
                    f"inválidas: {sorted(sobrando)}."
                ),
            )

        trilhas = self.trilha_repo.listar_ativas()
        scores: list[tuple[Trilha, float]] = []
        for trilha in trilhas:
            soma_ponderada = 0.0
            soma_pesos = 0.0
            for ptp in trilha.pesos_perguntas:
                resposta = respostas_map.get(ptp.pergunta_id, 0)
                soma_ponderada += resposta * ptp.peso
                soma_pesos += ptp.peso
            if soma_pesos == 0:
                continue
            score = soma_ponderada / (5 * soma_pesos)
            scores.append((trilha, score))

        if not scores:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Nenhuma trilha possui pesos calibrados — peça à COMGRAD "
                    "para revisar as trilhas antes de solicitar."
                ),
            )

        scores.sort(key=lambda item: item[1], reverse=True)
        return self._aplicar_indicador_confianca(scores)

    @classmethod
    def _aplicar_indicador_confianca(
        cls, scores: list[tuple[Trilha, float]]
    ) -> list[Trilha]:
        if len(scores) <= cls.N_MIN_CANDIDATAS:
            return [trilha for trilha, _ in scores]

        gap = scores[0][1] - scores[1][1]
        if gap >= cls.GAP_PERFIL_DECIDIDO:
            n = cls.N_MIN_CANDIDATAS
        elif gap >= cls.GAP_PERFIL_DEFINIDO:
            n = 3
        else:
            n = cls.N_MAX_CANDIDATAS

        n = min(n, len(scores))
        return [trilha for trilha, _ in scores[:n]]

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

    def _validar_pesos(
        self, pesos: list[PesoPerguntaInput]
    ) -> list[tuple[int, float]]:
        perguntas_ativas = self.pergunta_repo.listar_ativas()
        ids_obrigatorios = {p.id for p in perguntas_ativas}
        if not ids_obrigatorios:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Não há perguntas ativas cadastradas — cadastre-as antes "
                    "de criar ou editar trilhas."
                ),
            )

        vistos: dict[int, float] = {}
        for p in pesos:
            if p.pergunta_id in vistos:
                raise HTTPException(
                    status_code=400,
                    detail=f"Peso duplicado para pergunta {p.pergunta_id}.",
                )
            vistos[p.pergunta_id] = p.peso

        faltando = ids_obrigatorios - vistos.keys()
        sobrando = vistos.keys() - ids_obrigatorios
        if faltando or sobrando:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Pesos não cobrem exatamente as perguntas ativas. "
                    f"Faltando: {sorted(faltando)}; "
                    f"inválidas/inativas: {sorted(sobrando)}."
                ),
            )

        return list(vistos.items())
