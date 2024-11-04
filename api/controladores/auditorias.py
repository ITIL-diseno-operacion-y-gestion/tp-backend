from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, eliminar_por_id
from ..modelo.usuario import (
    Usuario,
    UsuarioPublico,
    UsuarioForm,
    UsuarioLoginForm,
    UsuarioLoginRespuesta,
)
from ..modelo.auditoria import Auditoria, registrar_accion, ACCION_CREACION
import secrets
import string

router = APIRouter(
    prefix="/auditorias",
    tags=["auditorias"],
)

@router.get("")
def obtener_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Auditoria)).all()


@router.get("/{id}")
def obtener_usuarios(id, entidad: str, session: Session = Depends(get_session)):
    query = select(Auditoria)
    query = query.where(Auditoria.clase_entidad == entidad)
    query = query.where(Auditoria.id_entidad == id)
    print("filtro por id: ", id)
    return session.exec(query).all()

