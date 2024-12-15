from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class Rol(Enum):
    CLIENTE = "cliente"
    AGENTE = "agente"
    SUPERVISOR = "supervisor"


class UsuarioBase(SQLModel):
    nombre: str
    apellido: str
    email: str
    rol: Rol


class UsuarioForm(UsuarioBase):
    contrasenia: str


class UsuarioPublico(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str
    rol: Rol


class UsuarioLoginForm(SQLModel):
    email: Optional[str] = None
    contrasenia: Optional[str] = None


class UsuarioLoginRespuesta(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str
    token: str
    rol: str


class Usuario(UsuarioForm, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
