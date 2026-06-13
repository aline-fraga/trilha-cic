from fastapi import HTTPException
from sqlalchemy.orm import Session

from server.models.disciplina import Disciplina
from server.repositories.disciplina_repository import DisciplinaRepository
from server.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate


class DisciplinaService:
    def __init__(self, db: Session):
        self.repo = DisciplinaRepository(db)

    def listar(self, is_active: bool | None = None) -> list[Disciplina]:
        return self.repo.listar(is_active=is_active)

    def buscar(self, disciplina_id: int) -> Disciplina:
        disciplina = self.repo.get_by_id(disciplina_id)
        if not disciplina or not disciplina.is_active:
            raise HTTPException(
                status_code=404, detail="Disciplina não encontrada"
            )
        return disciplina

    def criar(self, data: DisciplinaCreate) -> Disciplina:
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Já existe uma disciplina com o código '{data.codigo}'"
                ),
            )
        disciplina = Disciplina(
            nome=data.nome,
            codigo=data.codigo,
            tipo=data.tipo,
            carga_horaria=data.carga_horaria,
            link_plano_ensino=data.link_plano_ensino,
        )
        return self.repo.criar(disciplina)

    def atualizar(
        self, disciplina_id: int, data: DisciplinaUpdate
    ) -> Disciplina:
        disciplina = self.buscar(disciplina_id)

        if data.codigo and data.codigo != disciplina.codigo:
            existente = self.repo.get_by_codigo(data.codigo)
            if existente:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Já existe uma disciplina com o código '{data.codigo}'"
                    ),
                )

        return self.repo.atualizar(
            disciplina,
            nome=data.nome,
            codigo=data.codigo,
            tipo=data.tipo,
            carga_horaria=data.carga_horaria,
            link_plano_ensino=data.link_plano_ensino,
        )

    def excluir(self, disciplina_id: int) -> None:
        disciplina = self.buscar(disciplina_id)
        self.repo.inativar(disciplina)
