from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import SugestaoTrilha
from server.models.enums import UserRole
from server.models.user import User
from server.schemas.responses import (
    BAD_REQUEST_400,
    FORBIDDEN_403,
    NOT_FOUND_404,
    UNAUTHORIZED_401,
)
from server.schemas.chamado import ChamadoResponse
from server.schemas.sugestao_trilha import (
    SugestaoTrilhaCreate,
    SugestaoTrilhaResponse,
)
from server.services.auth_service import get_current_user, require_roles
from server.services.sugestao_trilha_service import SugestaoTrilhaService
from server.services.user_service import UserService


class SugestaoTrilhaController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/sugestoes-trilha", tags=["sugestoes-trilha"]
        )

        self.router.add_api_route(
            "/create",
            self.criar_sugestao,
            methods=["POST"],
            response_model=SugestaoTrilhaResponse,
            status_code=status.HTTP_201_CREATED,
            dependencies=[require_roles(UserRole.ALUNO)],
            summary="Sugerir nova trilha acadêmica (ALUNO)",
            description=(
                "Registra uma sugestão de nova trilha proposta pelo aluno e abre "
                "automaticamente um chamado do tipo `NOVA_TRILHA` para a COMGRAD "
                "avaliar.\n\n"
                "**Regras:**\n"
                "- Entre 1 e 4 disciplinas, todas ativas no catálogo.\n"
                "- O aluno não pode ter outro chamado `NOVA_TRILHA` em aberto "
                "(retorna 400 se houver)."
            ),
            responses={
                400: BAD_REQUEST_400,
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
            },
        )

        self.router.add_api_route(
            "/get",
            self.listar_sugestoes,
            methods=["GET"],
            response_model=list[SugestaoTrilhaResponse],
            dependencies=[Depends(get_current_user)],
            summary="Listar sugestões de trilha",
            description=(
                "Retorna as sugestões de trilha ordenadas por data de criação "
                "decrescente. ALUNO vê apenas as próprias sugestões; COMGRAD vê "
                "todas as registradas no sistema."
            ),
            responses={401: UNAUTHORIZED_401},
        )

        self.router.add_api_route(
            "/get/{sugestao_id}",
            self.obter_sugestao,
            methods=["GET"],
            response_model=SugestaoTrilhaResponse,
            dependencies=[Depends(get_current_user)],
            summary="Obter sugestão de trilha por ID",
            description=(
                "Retorna os dados completos de uma sugestão, incluindo a lista de "
                "disciplinas e o `chamado_id` associado. ALUNO só pode obter "
                "sugestões próprias (403 caso contrário)."
            ),
            responses={
                401: UNAUTHORIZED_401,
                403: FORBIDDEN_403,
                404: NOT_FOUND_404,
            },
        )

    def criar_sugestao(
        self,
        payload: SugestaoTrilhaCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SugestaoTrilhaService(db)
        sugestao = service.sugerir(
            aluno_id=current_user.id,
            nome=payload.nome,
            disciplinas_ids=payload.disciplinas_ids,
        )
        return self._montar_response(sugestao, db)

    def listar_sugestoes(
        self,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SugestaoTrilhaService(db)
        aluno_filter = (
            current_user.id if current_user.role == UserRole.ALUNO else None
        )
        sugestoes = service.listar(aluno_id=aluno_filter)
        user_service = UserService(db)
        cache: dict[int, User | None] = {}
        return [self._montar_response(s, db, user_service, cache) for s in sugestoes]

    def obter_sugestao(
        self,
        sugestao_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service = SugestaoTrilhaService(db)
        sugestao = service.obter(sugestao_id)
        if (
            current_user.role == UserRole.ALUNO
            and sugestao.aluno_id != current_user.id
        ):
            raise HTTPException(status_code=403, detail="Acesso negado")
        return self._montar_response(sugestao, db)

    @staticmethod
    def _montar_response(
        sugestao: SugestaoTrilha,
        db: Session,
        user_service: UserService | None = None,
        cache: dict[int, User | None] | None = None,
    ) -> SugestaoTrilhaResponse:
        user_service = user_service or UserService(db)
        if cache is not None:
            if sugestao.aluno_id not in cache:
                cache[sugestao.aluno_id] = user_service.obter(sugestao.aluno_id)
            aluno = cache[sugestao.aluno_id]
        else:
            aluno = user_service.obter(sugestao.aluno_id)
        nome_aluno = aluno.nome if aluno else "Desconhecido"
        chamado_db = sugestao.chamado
        chamado_response = ChamadoResponse(
            id=chamado_db.id,
            aluno_id=chamado_db.aluno_id,
            aluno_nome=nome_aluno,
            tipo=chamado_db.tipo,
            assunto=chamado_db.assunto,
            mensagem=chamado_db.mensagem,
            status=chamado_db.status,
            resposta=chamado_db.resposta,
            respondido_em=chamado_db.respondido_em,
            trilha_id=chamado_db.trilha_id,
            created_at=chamado_db.created_at,
            updated_at=chamado_db.updated_at,
        )
        return SugestaoTrilhaResponse(
            id=sugestao.id,
            nome_proposto=sugestao.nome_proposto,
            aluno_id=sugestao.aluno_id,
            aluno_nome=nome_aluno,
            chamado=chamado_response,
            disciplinas=sugestao.disciplinas,
            created_at=sugestao.created_at,
        )
