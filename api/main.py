from fastapi import FastAPI

from .db import init_db
from .controladores import usuarios, configuracion, incidentes, problemas, cambios


app = FastAPI()
app.include_router(usuarios.router)
app.include_router(configuracion.router)
app.include_router(incidentes.router)
app.include_router(problemas.router)
app.include_router(cambios.router)


@app.on_event("startup")
def on_startup():
    init_db()
