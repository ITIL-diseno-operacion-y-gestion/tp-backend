from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

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

class UsuarioLoginForm(BaseModel):
    email: Optional[str] = None
    contrasenia: Optional[str] = None

class UsuarioLoginRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    token: str


class Usuario(UsuarioForm, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
