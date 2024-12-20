from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id, eliminar_por_id
from ..modelo.cambio import Cambio, CambioForm, CambioPublico, CambioUpdateForm
from ..modelo.usuario import Usuario
from ..modelo.articulo import Articulo
from datetime import datetime
from ..modelo.auditoria import (
    registrar_accion,
    ACCION_CREACION,
    ACCION_ELIMINACION,
    ACCION_ACTUALIZACION,
)

router = APIRouter(
    prefix="/cambios",
    tags=["Gestión de cambios"],
)

CLASE_CAMBIO = "cambio"


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
    registrar_accion(session, CLASE_CAMBIO, cambio.id, ACCION_CREACION, cambio.json())
    return cambio


@router.get("/{id}", response_model=CambioPublico)
def obtener_cambio(id, session: Session = Depends(get_session)):
    return obtener_por_id(Cambio, id, session)


@router.patch("/{id}")
def actualizar_cambio(
    id, cambio_form: CambioUpdateForm, session: Session = Depends(get_session)
):
    cambio = obtener_por_id(Cambio, id, session)
    cambio_nueva_data = cambio_form.model_dump(exclude_unset=True)

    cambio.sqlmodel_update(cambio_nueva_data)
    session.add(cambio)
    session.commit()
    session.refresh(cambio)
    cambio_respuesta = cambio.copy()
    registrar_accion(
        session, CLASE_CAMBIO, cambio.id, ACCION_ACTUALIZACION, cambio.json()
    )
    return cambio_respuesta


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cambio(id, session: Session = Depends(get_session)):
    eliminar_por_id(Cambio, id, session)
    registrar_accion(session, CLASE_CAMBIO, id, ACCION_ELIMINACION, "")
