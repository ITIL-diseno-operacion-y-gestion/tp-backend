from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..modelo.usuario import Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get("")
def obtener_usuarios(session: Session = Depends(get_session)):
    usuarios = session.exec(select(Usuario)).all()
    return usuarios


@router.post("")
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario
