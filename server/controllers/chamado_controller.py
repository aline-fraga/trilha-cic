from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.chamado import ChamadoCreate, ChamadoResponse, ChamadoResponder
from server.services.chamado_service import ChamadoService


class ChamadoController:
    def __init__(self):
        self.router = APIRouter(prefix="/chamados", tags=["chamados"])

        self.router.add_api_route(
            "",
            self.abrir_chamado,
            methods=["POST"],
            response_model=ChamadoResponse,
            status_code=201,
        )

        self.router.add_api_route(
            "",
            self.listar_chamados,
            methods=["GET"],
            response_model=list[ChamadoResponse],
        )

        self.router.add_api_route(
            "/{chamado_id}/responder",
            self.responder_chamado,
            methods=["PUT"],
            response_model=ChamadoResponse,
        )

    def abrir_chamado(
        self,
        dados: ChamadoCreate,
        db: Session = Depends(get_db),
    ):
        service = ChamadoService(db)

        aluno_id = 1

        # REMOVER COMENTARIO APOS TESTES
        # return service.criar(dados, aluno_id)
        
        # MOCK DATA
        c = service.criar(dados, aluno_id)
        c_dict = {
            "id": c.id,
            "aluno_id": c.aluno_id,
            "aluno_nome": "mariana.ercolani@ufrgs.br" if c.aluno_id == 1 else "pedro.kuhn@ufrgs.br",
            "tipo": c.tipo,
            "assunto": c.assunto,
            "mensagem": c.mensagem,
            "status": c.status,
            "resposta": c.resposta,
            "respondido_em": c.respondido_em,
            "trilha_id": c.trilha_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        return ChamadoResponse(**c_dict)

    def listar_chamados(
        self,
        status: str | None = None,
        db: Session = Depends(get_db),
    ):
        service = ChamadoService(db)
        
        # REMOVER COMENTARIO APOS TESTES
        # return service.listar(status)
        
        # MOCK DATA
        chamados_db = service.listar(status)
        res = []
        for c in chamados_db:
            c_dict = {
                "id": c.id,
                "aluno_id": c.aluno_id,
                "aluno_nome": "mariana.ercolani@ufrgs.br" if c.aluno_id == 1 else "pedro.kuhn@ufrgs.br",
                "tipo": c.tipo,
                "assunto": c.assunto,
                "mensagem": c.mensagem,
                "status": c.status,
                "resposta": c.resposta,
                "respondido_em": c.respondido_em,
                "trilha_id": c.trilha_id,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
            }
            res.append(ChamadoResponse(**c_dict))
            
        return res

    def responder_chamado(
        self,
        chamado_id: int,
        dados: ChamadoResponder,
        db: Session = Depends(get_db),
    ):
        service = ChamadoService(db)
        
        # MOCK ADMIN_ID
        admin_id = 2
        
        c = service.atualizar(chamado_id, dados.resposta, admin_id)
        
        c_dict = {
            "id": c.id,
            "aluno_id": c.aluno_id,
            "aluno_nome": "mariana.ercolani@ufrgs.br" if c.aluno_id == 1 else "pedro.kuhn@ufrgs.br",
            "tipo": c.tipo,
            "assunto": c.assunto,
            "mensagem": c.mensagem,
            "status": c.status,
            "resposta": c.resposta,
            "respondido_em": c.respondido_em,
            "trilha_id": c.trilha_id,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        return ChamadoResponse(**c_dict)
