from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from server.models.disciplina import Disciplina
from server.repositories.disciplina_repository import DisciplinaRepository
from server.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate


class DisciplinaService:
    def __init__(self, db: Session):
        self.repo = DisciplinaRepository(db)

    def listar(self) -> list[Disciplina]:
        return self.repo.listar_ativas()

    def buscar(self, disciplina_id: int) -> Disciplina:
        disciplina = self.repo.get_by_id(disciplina_id)
        if not disciplina or not disciplina.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina não encontrada")
        return disciplina

    def criar(self, data: DisciplinaCreate) -> Disciplina:
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"campo": "codigo", "mensagem": f"Já existe uma disciplina com o código '{data.codigo}'"},
            )
        disciplina = Disciplina(
            nome=data.nome,
            codigo=data.codigo,
            carga_horaria=data.carga_horaria,
        )
        return self.repo.criar(disciplina)

    def atualizar(self, disciplina_id: int, data: DisciplinaUpdate) -> Disciplina:
        disciplina = self.buscar(disciplina_id)

        if data.codigo and data.codigo != disciplina.codigo:
            existente = self.repo.get_by_codigo(data.codigo)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={"campo": "codigo", "mensagem": f"Já existe uma disciplina com o código '{data.codigo}'"},
                )

        if data.nome is not None:
            disciplina.nome = data.nome
        if data.codigo is not None:
            disciplina.codigo = data.codigo
        if data.carga_horaria is not None:
            disciplina.carga_horaria = data.carga_horaria

        return disciplina

    def excluir(self, disciplina_id: int) -> None:
        disciplina = self.buscar(disciplina_id)
        self.repo.inativar(disciplina)
