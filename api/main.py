from fastapi import FastAPI

from .db import init_db
from .controladores import usuarios, configuracion, incidentes, problemas, cambios, reportes, auditorias


app = FastAPI(
    title="ITIL API",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "arta"},
        "tryItOutEnabled": True,
    },
)
app.include_router(usuarios.router)
app.include_router(configuracion.router)
app.include_router(incidentes.router)
app.include_router(problemas.router)
app.include_router(cambios.router)
app.include_router(reportes.router)
app.include_router(auditorias.router)


@app.on_event("startup")
def on_startup():
    init_db()
