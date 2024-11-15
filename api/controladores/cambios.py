from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id, eliminar_por_id
from ..modelo.cambio import Cambio, CambioForm, CambioPublico
from ..modelo.usuario import Usuario
from ..modelo.articulo import Articulo
from datetime import datetime
from ..modelo.auditoria import registrar_accion, ACCION_CREACION, ACCION_ELIMINACION

router = APIRouter(
    prefix="/cambios",
    tags=["Gestión de cambios"],
)

CLASE_CAMBIO = "cambio"

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cambio_por_id(id, session: Session = Depends(get_session)):
    eliminar_por_id(Cambio, id, session)
    registrar_accion(session, CLASE_CAMBIO, id, ACCION_ELIMINACION, None, None)

@router.get("/{id}", response_model=CambioPublico)
def obtener_cambio_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(Cambio, id, session)


@router.get("")
def obtener_cambios(session: Session = Depends(get_session)):
    cambios = session.exec(select(Cambio)).all()
    return cambios


@router.post("", response_model=CambioPublico)
def crear_cambio(cambio_form: CambioForm, session: Session = Depends(get_session)):
    usuario = obtener_por_id(Usuario, cambio_form.id_solicitante, session)

    if len(cambio_form.ids_articulos) < 1:
        raise HTTPException(
            status_code=422, detail="Se debe ingresar al menos un articulo"
        )

    articulos = session.exec(
        select(Articulo).where(Articulo.id.in_(cambio_form.ids_articulos))
    ).all()

    if len(articulos) != len(cambio_form.ids_articulos):
        raise HTTPException(
            status_code=422, detail="Alguno de los articulos no fue encontrado"
        )

    cambio = Cambio.model_validate(cambio_form)
    cambio.fecha_de_creacion = datetime.now()
    cambio.articulos_afectados = articulos

    session.add(cambio)
    session.commit()
    session.refresh(cambio)
    registrar_accion(session, CLASE_CAMBIO, cambio.id, ACCION_CREACION, None, cambio.json())
    return cambio
