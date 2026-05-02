from fastapi import FastAPI

from server.controllers.trilha_controller import TrilhaController

app = FastAPI(title="TrilhaCiC API")

trilha_controller = TrilhaController()
app.include_router(trilha_controller.router)
