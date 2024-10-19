from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.problema import Problema, ProblemaForm, ProblemaPublico, Estado, ProblemaUpdateForm
from ..modelo.incidente import Incidente

router = APIRouter(
    prefix="/problemas",
    tags=["problemas"],
)


@router.get("/{id}", response_model=ProblemaPublico)
def obtener_problema_por_id(id, session: Session = Depends(get_session)):
    problema = session.get_one(Problema, id)
    return problema


@router.get("", response_model=list[Problema])
def obtener_problemas(session: Session = Depends(get_session)):
    problemas = session.exec(select(Problema)).all()
    return problemas


@router.post("", response_model=ProblemaPublico)
def crear_problema(
    problema_form: ProblemaForm, session: Session = Depends(get_session)
):
    incidentes = session.exec(
        select(Incidente).where(Incidente.id.in_(problema_form.ids_incidentes))
    ).all()
    problema = Problema.model_validate(problema_form)
    problema.incidentes = incidentes
    session.add(problema)
    session.commit()
    session.refresh(problema)
    return problema

@router.patch("/{id}", response_model=ProblemaPublico)
def actualizar_problema(
    id, problema_form: ProblemaUpdateForm, session: Session = Depends(get_session)
):
    problema = session.get_one(Problema, id)
    if not problema:
         raise HTTPException(status_code=404, detail="Problema not found")
    problema_nueva_data = problema_form.model_dump(exclude_unset=True)
    problema.sqlmodel_update(problema_nueva_data)
    session.add(problema)
    session.commit()
    session.refresh(problema)
    return problema