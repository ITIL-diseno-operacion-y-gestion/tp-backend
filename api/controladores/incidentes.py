from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.incidente import Incidente
from ..modelo.usuario import Usuario
from datetime import datetime

router = APIRouter(
    prefix="/incidentes",
    tags=["incidentes"],
)


@router.get("")
def obtener_incidentes(session: Session = Depends(get_session)):
    incidentes = session.exec(select(Incidente)).all()
    return incidentes


@router.post("")
def crear_incidente(incidente: Incidente, session: Session = Depends(get_session)):
    incidente.id = None
    incidente.fecha_de_alta = datetime.now()

    usuario = session.exec(
        select(Usuario).where(Usuario.id == incidente.id_usuario)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {incidente.id_usuario} no existe"
        )

    session.add(incidente)
    session.commit()
    session.refresh(incidente)
    return incidente
