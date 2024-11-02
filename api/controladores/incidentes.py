from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id
from ..modelo.incidente import Incidente, IncidenteForm, IncidentePublico
from ..modelo.articulo import Articulo
from ..modelo.usuario import Usuario
from datetime import datetime

router = APIRouter(
    prefix="/incidentes",
    tags=["Gestión de incidentes"],
)


@router.get("/{id}", response_model=IncidentePublico)
def obtener_incidente_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(Incidente, id, session)


@router.get("")
def obtener_incidentes(session: Session = Depends(get_session)):
    incidentes = session.exec(select(Incidente)).all()
    return incidentes


@router.post("", response_model=IncidentePublico)
def crear_incidente(
    incidente_form: IncidenteForm, session: Session = Depends(get_session)
):
    print("incidente_form.ids_articulos: ", incidente_form.ids_articulos)
    print("incidente_form.conformidad_resolucion: ", incidente_form.conformidad_resolucion)
    if len(incidente_form.ids_articulos) < 1:
        raise HTTPException(
            status_code=422, detail="Se debe ingresar al menos un articulo"
        )

    articulos = session.exec(
        select(Articulo).where(Articulo.id.in_(incidente_form.ids_articulos))
    ).all()

    if len(articulos) != len(incidente_form.ids_articulos):
        raise HTTPException(
            status_code=422, detail="Alguno de los articulos no fue encontrado"
        )

    usuario = obtener_por_id(Usuario, incidente_form.id_usuario, session)

    incidente = Incidente.model_validate(incidente_form)
    incidente.articulos_afectados = articulos
    incidente.fecha_de_alta = datetime.now()

    session.add(incidente)
    session.commit()
    session.refresh(incidente)
    return incidente
