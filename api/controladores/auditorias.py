from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.auditoria import Auditoria

router = APIRouter(
    prefix="/auditorias",
    tags=["Auditorías"],
)


@router.get("")
def obtener_auditorias(session: Session = Depends(get_session)):
    return session.exec(select(Auditoria)).all()


@router.get("/{id}")
def obtener_auditoria(id, entidad: str, session: Session = Depends(get_session)):
    query = select(Auditoria)
    query = query.where(Auditoria.clase_entidad == entidad)
    query = query.where(Auditoria.id_entidad == id)
    print("filtro por id: ", id)
    return session.exec(query).all()
