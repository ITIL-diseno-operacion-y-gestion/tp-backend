from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, obtener_por_id, eliminar_por_id
from ..modelo.incidente import (
    Incidente,
    IncidenteForm,
    IncidentePatchForm,
    IncidentePublico,
)
from ..modelo.articulo import Articulo
from ..modelo.usuario import Usuario, UsuarioPublico, Rol
from datetime import datetime
from ..modelo.auditoria import (
    registrar_accion,
    ACCION_CREACION,
    ACCION_ELIMINACION,
    ACCION_ACTUALIZACION,
)
from typing import Optional

router = APIRouter(
    prefix="/incidentes",
    tags=["Gestión de incidentes"],
)

CLASE_INCIDENTE = "incidente"


@router.get("")
def obtener_incidentes(
    id_usuario: Optional[int] = None, session: Session = Depends(get_session)
):
    query = select(Incidente)
    if id_usuario is not None:
        query = query.where(Incidente.id_usuario == id_usuario)
    incidentes = session.exec(query).all()
    incidentes_dict = []
    for incidente in incidentes:
        agente_asignado = session.exec(
            select(Usuario).where(Usuario.id == incidente.id_agente_asignado)
        ).first()
        incidente_dict = incidente.__dict__
        incidente_dict.pop("id_agente_asignado")
        incidente_dict["agente_asignado"] = (
            UsuarioPublico.model_validate(agente_asignado) if agente_asignado else None
        )
        incidentes_dict.append(incidente_dict)
    return incidentes_dict


@router.post("", response_model=IncidentePublico)
def crear_incidente(
    incidente_form: IncidenteForm, session: Session = Depends(get_session)
):
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
    agente_asignado = (
        obtener_por_id(Usuario, incidente_form.id_agente_asignado, session)
        if incidente_form.id_agente_asignado
        else None
    )
    if agente_asignado and agente_asignado.rol == Rol.CLIENTE:
        raise HTTPException(
            status_code=403, detail="El usuario asignado no es agente ni supervisor"
        )

    incidente = Incidente.model_validate(incidente_form)
    incidente.articulos_afectados = articulos
    incidente.fecha_de_alta = datetime.now()

    session.add(incidente)
    session.commit()
    session.refresh(incidente)
    registrar_accion(
        session, CLASE_INCIDENTE, incidente.id, ACCION_CREACION, incidente.json()
    )
    return incidente


@router.get("/{id}")
def obtener_incidente(id, session: Session = Depends(get_session)):
    incidente = obtener_por_id(Incidente, id, session)
    incidente_dict = incidente.__dict__

    agente_asignado = (
        session.exec(
            select(Usuario).where(Usuario.id == incidente.id_agente_asignado)
        ).first()
        if incidente.id_agente_asignado
        else None
    )

    incidente_dict["agente_asignado"] = (
        UsuarioPublico.model_validate(agente_asignado) if agente_asignado else None
    )
    incidente_dict.pop("id_agente_asignado")
    return incidente_dict


@router.patch("/{id}", response_model=IncidentePublico)
def modificar_incidente(
    id, incidente_form: IncidentePatchForm, session: Session = Depends(get_session)
):
    incidente = obtener_por_id(Incidente, id, session)
    incidente_actualizado = incidente_form.model_dump(exclude_unset=True)
    agente_asignado = obtener_por_id(
        Usuario, incidente_form.id_agente_asignado, session
    )
    if agente_asignado and agente_asignado.rol == Rol.CLIENTE:
        raise HTTPException(
            status_code=403, detail="El usuario asignado no es agente ni supervisor"
        )

    incidente.sqlmodel_update(incidente_actualizado)

    session.add(incidente)
    session.commit()
    session.refresh(incidente)
    incidente_respuesta = IncidentePublico.from_orm(incidente)
    registrar_accion(
        session, CLASE_INCIDENTE, incidente.id, ACCION_ACTUALIZACION, incidente.json()
    )
    return incidente_respuesta


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_incidente(id, session: Session = Depends(get_session)):
    eliminar_por_id(Incidente, id, session)
    registrar_accion(session, CLASE_INCIDENTE, id, ACCION_ELIMINACION, "")
