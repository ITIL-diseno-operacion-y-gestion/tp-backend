from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id, eliminar_por_id
from ..modelo.problema import (
    Problema,
    ProblemaForm,
    ProblemaUpdateForm,
    ProblemaPublico,
    Estado,
)
from ..modelo.incidente import Incidente
from ..modelo.error_conocido import (
    ErrorConocido,
    ErrorConocidoForm,
    ErrorConocidoPublico,
)
from datetime import datetime
from ..modelo.auditoria import registrar_accion, ACCION_CREACION, ACCION_ACTUALIZACION, ACCION_ELIMINACION

CLASE_PROBLEMA = "problema"
CLASE_ERROR = "error"

router = APIRouter(tags=["Gestión de problemas"])

@router.delete("/problemas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_problema_por_id(id, session: Session = Depends(get_session)):
    eliminar_por_id(Problema, id, session)
    registrar_accion(session, CLASE_PROBLEMA, id, ACCION_ELIMINACION, None, None)

@router.get("/problemas/{id}", response_model=ProblemaPublico)
def obtener_problema_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(Problema, id, session)


@router.get("/problemas", response_model=list[Problema])
def obtener_problemas(session: Session = Depends(get_session)):
    return session.exec(select(Problema)).all()


@router.post("/problemas", response_model=ProblemaPublico)
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
    registrar_accion(session, CLASE_PROBLEMA, problema.id, ACCION_CREACION, None, problema.json())
    return problema


@router.patch("/problemas/{id}")
def actualizar_problema(
    id, problema_form: ProblemaUpdateForm, session: Session = Depends(get_session)
):
    problema = obtener_por_id(Problema, id, session)
    estado_anterior = problema.json()
    problema_nueva_data = problema_form.model_dump(exclude_unset=True)
    if problema.estado != Estado.RESUELTO and problema_form.estado == Estado.RESUELTO:
        problema_nueva_data["fecha_de_resolucion"] = datetime.now()
    problema.sqlmodel_update(problema_nueva_data)
    session.add(problema)
    session.commit()
    session.refresh(problema)
    problema_respuesta = problema.copy()
    registrar_accion(session, CLASE_PROBLEMA, problema.id, ACCION_ACTUALIZACION, estado_anterior, problema.json())
    return problema_respuesta


@router.delete("/errores-conocidos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_error_conocido_por_id(id, session: Session = Depends(get_session)):
    eliminar_por_id(ErrorConocido, id, session)
    registrar_accion(session, CLASE_ERROR, id, ACCION_ELIMINACION, None, None)

@router.get("/errores-conocidos/{id}", response_model=ErrorConocidoPublico)
def obtener_error_conocido_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(ErrorConocido, id, session)


@router.get("/errores-conocidos")
def obtener_errores_conocidos(session: Session = Depends(get_session)):
    return session.exec(select(ErrorConocido)).all()


@router.post("/errores-conocidos", response_model=ErrorConocidoPublico)
def crear_error_conocido(
    error_conocido_form: ErrorConocidoForm,
    session: Session = Depends(get_session),
):
    incidentes = session.exec(
        select(Incidente).where(Incidente.id.in_(error_conocido_form.ids_incidentes))
    ).all()

    if len(incidentes) != len(error_conocido_form.ids_incidentes):
        raise HTTPException(
            status_code=422, detail="Alguno de los incidentes no fue encontrado"
        )

    problemas = session.exec(
        select(Problema).where(Problema.id.in_(error_conocido_form.ids_problemas))
    ).all()

    if len(problemas) != len(error_conocido_form.ids_problemas):
        raise HTTPException(
            status_code=422, detail="Alguno de los problemas no fue encontrado"
        )

    error_conocido = ErrorConocido.model_validate(error_conocido_form)
    error_conocido.incidentes = incidentes
    error_conocido.problemas = problemas
    error_conocido.fecha_de_creacion = datetime.now()

    session.add(error_conocido)
    session.commit()
    session.refresh(error_conocido)
    registrar_accion(session, CLASE_ERROR, error_conocido.id, ACCION_CREACION, None, error_conocido.json())
    return error_conocido
