from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.controllers.auth_controller import AuthController
from server.controllers.curriculo_controller import CurriculoController
from server.controllers.relatorio_controller import RelatorioController
from server.controllers.trilha_controller import TrilhaController
from server.controllers.user_controller import UserController

app = FastAPI(title="TrilhaCiC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trilha_controller = TrilhaController()
auth_controller = AuthController()
curriculo_controller = CurriculoController()
user_controller = UserController()

app.include_router(trilha_controller.router)
app.include_router(auth_controller.router)
app.include_router(curriculo_controller.router)

relatorio_controller = RelatorioController()
app.include_router(relatorio_controller.router)
app.include_router(user_controller.router)
