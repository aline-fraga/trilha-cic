from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from server.models import Disciplina, PerguntaTrilhaPeso, Trilha, trilha_disciplinas


class TrilhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_ativas(self) -> list[Trilha]:
        stmt = (
            select(Trilha)
            .where(Trilha.is_active.is_(True))
            .options(
                selectinload(Trilha.disciplinas),
                selectinload(Trilha.pesos_perguntas),
            )
        )
        return list(self.db.scalars(stmt))

    def listar_por_disciplinas_ids(self, ids: list[int]) -> list[Trilha]:
        if not ids:
            return []
        stmt = (
            select(Trilha)
            .join(trilha_disciplinas, trilha_disciplinas.c.trilha_id == Trilha.id)
            .where(
                Trilha.is_active.is_(True),
                trilha_disciplinas.c.disciplina_id.in_(ids),
            )
            .distinct()
            .options(selectinload(Trilha.disciplinas))
        )
        return list(self.db.scalars(stmt))

    def obter(self, trilha_id: int) -> Trilha | None:
        stmt = (
            select(Trilha)
            .where(Trilha.id == trilha_id)
            .options(
                selectinload(Trilha.disciplinas),
                selectinload(Trilha.pesos_perguntas),
            )
        )
        return self.db.scalars(stmt).one_or_none()

    def criar(
        self,
        nome: str,
        resumo: str,
        disciplinas: list[Disciplina],
        pesos: list[tuple[int, float]],
    ) -> Trilha:
        trilha = Trilha(nome=nome, resumo=resumo, disciplinas=disciplinas)
        self.db.add(trilha)
        self.db.flush()
        for pergunta_id, peso in pesos:
            self.db.add(
                PerguntaTrilhaPeso(
                    pergunta_id=pergunta_id,
                    trilha_id=trilha.id,
                    peso=peso,
                )
            )
        self.db.commit()
        self.db.refresh(trilha)
        return trilha

    def atualizar(
        self,
        trilha: Trilha,
        nome: str | None = None,
        resumo: str | None = None,
        disciplinas: list[Disciplina] | None = None,
        pesos: list[tuple[int, float]] | None = None,
    ) -> Trilha:
        if nome is not None:
            trilha.nome = nome
        if resumo is not None:
            trilha.resumo = resumo
        if disciplinas is not None:
            trilha.disciplinas = disciplinas
        if pesos is not None:
            trilha.pesos_perguntas.clear()
            self.db.flush()
            for pergunta_id, peso in pesos:
                self.db.add(
                    PerguntaTrilhaPeso(
                        pergunta_id=pergunta_id,
                        trilha_id=trilha.id,
                        peso=peso,
                    )
                )
        self.db.commit()
        self.db.refresh(trilha)
        return trilha

    def soft_delete(self, trilha: Trilha) -> None:
        trilha.is_active = False
        self.db.commit()
