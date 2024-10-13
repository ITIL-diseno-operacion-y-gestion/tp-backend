from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.usuario import Usuario, UsuarioPublico, UsuarioForm

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get("", response_model=list[UsuarioPublico])
def obtener_usuarios(session: Session = Depends(get_session)):
    usuarios = session.exec(select(Usuario)).all()
    return usuarios


@router.post("")
def crear_usuario(usuario_form: UsuarioForm, session: Session = Depends(get_session)):
    usuario = Usuario.model_validate(usuario_form)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
