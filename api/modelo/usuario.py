from typing import Optional
from sqlmodel import SQLModel, Field


class UsuarioBase(SQLModel):
    nombre: str
    apellido: str
    email: str


class UsuarioForm(UsuarioBase):
    contrasenia: str


class UsuarioPublico(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str


class Usuario(UsuarioForm, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)