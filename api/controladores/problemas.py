from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id
from ..modelo.problema import (
    Problema,
    ProblemaForm,
    ProblemaUpdateForm,
    ProblemaPublico,
)
from ..modelo.incidente import Incidente
from datetime import datetime

router = APIRouter(
    prefix="/problemas",
    tags=["problemas"],
)


@router.get("/{id}", response_model=ProblemaPublico)
def obtener_problema_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(Problema, id, session)


@router.get("", response_model=list[Problema])
def obtener_problemas(session: Session = Depends(get_session)):
    problemas = session.exec(select(Problema)).all()
    return problemas


@router.post("", response_model=ProblemaPublico)
def crear_problema(
    problema_form: ProblemaForm, session: Session = Depends(get_session)
):
    if len(problema_form.ids_incidentes) < 1:
        raise HTTPException(
            status_code=422, detail="Se debe ingresar al menos un incidente"
        )

    incidentes = session.exec(
        select(Incidente).where(Incidente.id.in_(problema_form.ids_incidentes))
    ).all()

    if len(incidentes) != len(problema_form.ids_incidentes):
        raise HTTPException(
            status_code=422, detail="Alguno de los incidentes no fue encontrado"
        )

    problema = Problema.model_validate(problema_form)
    problema.incidentes = incidentes
    problema.fecha_de_deteccion = datetime.now()

    session.add(problema)
    session.commit()
    session.refresh(problema)
    return problema


@router.patch("/{id}")
def actualizar_problema(
    id, problema_form: ProblemaUpdateForm, session: Session = Depends(get_session)
):
    problema = obtener_por_id(Problema, id, session)
    problema_nueva_data = problema_form.model_dump(exclude_unset=True)
    problema.sqlmodel_update(problema_nueva_data)
    session.add(problema)
    session.commit()
    session.refresh(problema)
    return problema
