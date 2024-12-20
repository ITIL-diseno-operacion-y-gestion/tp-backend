from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id
from ..modelo.articulo import Articulo, ArticuloForm, ArticuloUpdate
from ..modelo.usuario import Usuario
from datetime import datetime
from ..modelo.auditoria import (
    registrar_accion,
    ACCION_CREACION,
    ACCION_ELIMINACION,
    ACCION_ACTUALIZACION,
)

router = APIRouter(
    prefix="/configuracion",
    tags=["Gestión de configuración"],
)

CLASE_ARTICULO = "articulo"


@router.get("/articulos")
def obtener_articulos(
    nombre: str | None = None, session: Session = Depends(get_session)
):
    query = select(Articulo).where(Articulo.esta_activo == True)
    if nombre:
        query = query.where(Articulo.nombre == nombre)
    articulos = session.exec(query).all()
    return articulos


@router.post("/articulos")
def crear_articulo(
    articulo_form: ArticuloForm, session: Session = Depends(get_session)
):
    usuario = obtener_por_id(Usuario, articulo_form.id_titular, session)
    articulo = Articulo.model_validate(articulo_form)
    articulo.fecha_de_alta = datetime.now()
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    articulo_respuesta = articulo.copy()
    registrar_accion(
        session, CLASE_ARTICULO, articulo.id, ACCION_CREACION, articulo.json()
    )
    return articulo_respuesta


@router.get("/articulos/{id}")
def obtener_articulo(id, session: Session = Depends(get_session)):
    return obtener_por_id(Articulo, id, session)


@router.patch("/articulos/{id}")
def actualizar_articulo(
    id, articulo_update: ArticuloUpdate, session: Session = Depends(get_session)
):
    articulo = obtener_por_id(Articulo, id, session)
    articulo_nueva_data = articulo_update.model_dump(exclude_unset=True)
    articulo.sqlmodel_update(articulo_nueva_data)
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    articulo_respuesta = articulo.copy()
    registrar_accion(
        session, CLASE_ARTICULO, articulo.id, ACCION_ACTUALIZACION, articulo.json()
    )
    return articulo_respuesta


@router.delete("/articulos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def dar_de_baja_articulo(id, session: Session = Depends(get_session)):
    articulo = obtener_por_id(Articulo, id, session)
    articulo.esta_activo = False
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    registrar_accion(session, CLASE_ARTICULO, id, ACCION_ELIMINACION, articulo.json())
    return articulo
