from .settings import DATABASE_URL
from sqlmodel import create_engine, SQLModel, Session, select
from fastapi import HTTPException

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def obtener_por_id(clase_entidad, id, session):
    entidad = session.exec(select(clase_entidad).where(clase_entidad.id == id)).first()
    if not entidad:
        raise HTTPException(
            status_code=404,
            detail=f"{clase_entidad.__name__} con id {id} no encontrado",
        )
    return entidad
