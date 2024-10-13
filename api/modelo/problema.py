from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class PrioridadDeProblema(Enum):
    MUY_BAJA = "muy baja"
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoDeProblema(Enum):
    DETECTADO = "detectado"
    EN_ANALISIS = "en analisis"
    ASIGNADO = "asignado"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"


class Problema(SQLModel, table=True):
    __tablename__ = "problemas"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    fecha_de_deteccion: str
    sintomas: str
    prioridad: str
    categoria: str
    estado: str
