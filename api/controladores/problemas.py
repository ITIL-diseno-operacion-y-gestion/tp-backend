from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.problema import Problema, ProblemaForm
from ..modelo.usuario import Usuario

router = APIRouter(
    prefix="/problemas",
    tags=["problemas"],
)


@router.get("")
def obtener_problemas(session: Session = Depends(get_session)):
    problemas = session.exec(select(Problema)).all()
    return problemas


@router.post("")
def crear_problema(
    problema_form: ProblemaForm, session: Session = Depends(get_session)
):
    problema = Problema.model_validate(problema_form)
    usuario = session.exec(
        select(Usuario).where(Usuario.id == problema.id_usuario)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {problema.id_usuario} no encontrado"
        )

    session.add(problema)
    session.commit()
    session.refresh(problema)
    return problema
