from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session, eliminar_por_id
from ..modelo.usuario import (
    Usuario,
    UsuarioPublico,
    UsuarioForm,
    UsuarioLoginForm,
    UsuarioLoginRespuesta,
    ROLES_VALIDOS,
)
from ..modelo.auditoria import registrar_accion, ACCION_CREACION, ACCION_ELIMINACION
import secrets
import string

CLASE_USUARIO = "usuario"

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario_por_id(id, session: Session = Depends(get_session)):
    eliminar_por_id(Usuario, id, session)
    registrar_accion(session, CLASE_USUARIO, id, ACCION_ELIMINACION, "")

@router.get("", response_model=list[UsuarioPublico])
def obtener_usuarios(session: Session = Depends(get_session)):
    print("entre a obtener_usuarios")
    usuarios = session.exec(select(Usuario)).all()
    return usuarios


@router.post("")
def crear_usuario(usuario_form: UsuarioForm, session: Session = Depends(get_session)):
    usuario = Usuario.model_validate(usuario_form)
    if usuario.rol not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=422,
            detail="rol invalido",
        )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    respuesta_usuario = usuario.copy()
    registrar_accion(session, CLASE_USUARIO, usuario.id, ACCION_CREACION, usuario.json(exclude={"contrasenia"}))
    return respuesta_usuario


def generar_random_token(length=32):
    characters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(characters) for _ in range(length))
    return token


@router.post("/login")
def login_usuario(
    usuario_form: UsuarioLoginForm, session: Session = Depends(get_session)
):
    usuario = session.exec(
        select(Usuario)
        .where(Usuario.email == usuario_form.email)
        .where(Usuario.contrasenia == usuario_form.contrasenia)
    ).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario con email y contraseña enviados no encontrado",
        )
    return UsuarioLoginRespuesta(
        id=usuario.id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        token=generar_random_token(),
        rol=usuario.rol
    )
