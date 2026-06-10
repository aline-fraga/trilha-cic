from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.controllers.auth_controller import AuthController
from server.controllers.disciplina_controller import DisciplinaController
from server.controllers.trilha_controller import TrilhaController

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
disciplina_controller = DisciplinaController()

app.include_router(trilha_controller.router)
app.include_router(auth_controller.router)
app.include_router(disciplina_controller.router)
