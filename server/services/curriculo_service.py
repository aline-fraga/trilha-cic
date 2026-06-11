from sqlalchemy.orm import Session

from server.models import Curriculo
from server.repositories.curriculo_repository import CurriculoRepository


class CurriculoService:
    def __init__(self, db: Session):
        self.curriculo_repo = CurriculoRepository(db)

    def listar(self, is_active: bool | None = None) -> list[Curriculo]:
        return self.curriculo_repo.listar(is_active=is_active)

    def obter(self, curriculo_id: int) -> Curriculo | None:
        return self.curriculo_repo.obter(curriculo_id)
