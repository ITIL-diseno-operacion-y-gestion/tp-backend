from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.incidente import Incidente, IncidenteForm
from ..modelo.usuario import Usuario

router = APIRouter(
    prefix="/incidentes",
    tags=["incidentes"],
)


@router.get("/{id}")
def obtener_incidente_por_id(id, session: Session = Depends(get_session)):
    incidente = session.get_one(Incidente, id)
    return incidente


@router.get("")
def obtener_incidentes(session: Session = Depends(get_session)):
    incidentes = session.exec(select(Incidente)).all()
    return incidentes


@router.post("")
def crear_incidente(
    incidente_form: IncidenteForm, session: Session = Depends(get_session)
):
    incidente = Incidente.model_validate(incidente_form)
    usuario = session.exec(
        select(Usuario).where(Usuario.id == incidente.id_usuario)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id {incidente.id_usuario} no encontrado",
        )

    session.add(incidente)
    session.commit()
    session.refresh(incidente)
    return incidente
