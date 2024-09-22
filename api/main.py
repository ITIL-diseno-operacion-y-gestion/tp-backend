from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, select
from .db import init_db, get_session
from .controladores import usuarios, configuracion, incidentes, problemas, cambios


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     secret_name: str
#     age: int | None = Field(default=None, index=True)


app = FastAPI()
app.include_router(usuarios.router)
app.include_router(configuracion.router)
app.include_router(incidentes.router)
app.include_router(problemas.router)
app.include_router(cambios.router)


@app.on_event("startup")
def on_startup():
    init_db()


# @app.get("/heroes")
# def get_heroes(session: Session = Depends(get_session)):
#     heroes = session.exec(select(Hero)).all()
#     return heroes


# @app.post("/heroes")
# def create_hero(hero: Hero, session: Session = Depends(get_session)):
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero
