from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

ROLES_VALIDOS = ["cliente", "supervisor", "agente"]


class UsuarioBase(SQLModel):
    nombre: str
    apellido: str
    email: str
    rol: str


class UsuarioForm(UsuarioBase):
    contrasenia: str


class UsuarioPublico(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol: str


class UsuarioLoginForm(BaseModel):
    email: Optional[str] = None
    contrasenia: Optional[str] = None


class UsuarioLoginRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    token: str
    rol: str


class Usuario(UsuarioForm, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
