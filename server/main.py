from fastapi import FastAPI

from server.controllers.curriculo_controller import CurriculoController
from server.controllers.trilha_controller import TrilhaController

app = FastAPI(title="TrilhaCiC API")

trilha_controller = TrilhaController()
app.include_router(trilha_controller.router)

curriculo_controller = CurriculoController()
app.include_router(curriculo_controller.router)
