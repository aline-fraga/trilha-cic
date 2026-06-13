from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.controllers.auth_controller import AuthController
from server.controllers.chamado_controller import ChamadoController
from server.controllers.curriculo_controller import CurriculoController
from server.controllers.disciplina_controller import DisciplinaController
from server.controllers.pergunta_controller import PerguntaController
from server.controllers.relatorio_controller import RelatorioController
from server.controllers.solicitacao_controller import SolicitacaoController
from server.controllers.sugestao_trilha_controller import SugestaoTrilhaController
from server.controllers.trilha_controller import TrilhaController
from server.controllers.user_controller import UserController

TAGS_METADATA = [
    {
        "name": "auth",
        "description": (
            "Autenticação e dados do usuário logado. `POST /auth/login` é o "
            "único endpoint público; os demais exigem `Authorization: Bearer <token>`."
        ),
    },
    {
        "name": "trilhas",
        "description": "Gestão e busca de trilhas acadêmicas (CRUD + pesquisa fuzzy).",
    },
    {
        "name": "curriculos",
        "description": "Consulta dos currículos cadastrados (grade curricular do curso).",
    },
    {
        "name": "users",
        "description": "Gestão de contas de usuários. **Acesso exclusivo do papel ADMIN.**",
    },
    {
        "name": "relatorios",
        "description": (
            "Relatórios de demanda de trilhas (aceites/rejeições por período). "
            "**Acesso exclusivo do papel COMGRAD.**"
        ),
    },
    {
        "name": "sugestoes-trilha",
        "description": (
            "Sugestões de novas trilhas propostas por alunos (UC13). Cada sugestão "
            "abre automaticamente um chamado `NOVA_TRILHA` para a COMGRAD."
        ),
    },
    {
        "name": "solicitacoes",
        "description": (
            "Solicitações de trilha personalizada (UC03/UC04/UC06): criação, "
            "listagem, aceite, rejeição e download do material. Cada aluno "
            "pode ter no máximo 1 trilha `ACEITA` e 1 solicitação `PENDENTE`."
        ),
    },
    {
        "name": "perguntas",
        "description": (
            "Perguntas do questionário vocacional usado em `POST "
            "/solicitacoes/create` (UC03). Escrita exclusiva da COMGRAD."
        ),
    },
]

API_DESCRIPTION = """
**TrilhaCiC** — Portal de Acompanhamento e Planejamento Acadêmico
(UFRGS / Instituto de Informática, Ciência da Computação).

API REST do backend, construída em **FastAPI + SQLAlchemy 2 + Pydantic v2**.

### Papéis do sistema
- **ALUNO** — solicita trilhas personalizadas, aceita/rejeita sugestões, abre chamados.
- **COMGRAD** — gerencia currículo e trilhas, responde chamados, gera relatórios.
- **ADMIN** — gerencia contas de usuários do sistema.

### Autenticação
Faça login em `POST /auth/login` para obter um JWT (`access_token`), e use-o como
`Authorization: Bearer <token>` nos endpoints protegidos.
"""

app = FastAPI(
    title="TrilhaCiC API",
    description=API_DESCRIPTION,
    version="0.5.0",
    openapi_tags=TAGS_METADATA,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trilha_controller = TrilhaController()
auth_controller = AuthController()
disciplina_controller = DisciplinaController()
curriculo_controller = CurriculoController()
user_controller = UserController()
relatorio_controller = RelatorioController()
chamado_controller = ChamadoController()
sugestao_trilha_controller = SugestaoTrilhaController()
solicitacao_controller = SolicitacaoController()
pergunta_controller = PerguntaController()

app.include_router(trilha_controller.router)
app.include_router(auth_controller.router)
app.include_router(disciplina_controller.router)
app.include_router(curriculo_controller.router)
app.include_router(relatorio_controller.router)
app.include_router(user_controller.router)
app.include_router(chamado_controller.router)
app.include_router(sugestao_trilha_controller.router)
app.include_router(solicitacao_controller.router)
app.include_router(pergunta_controller.router)
