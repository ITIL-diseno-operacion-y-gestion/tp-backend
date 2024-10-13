from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime


class PrioridadDeProblema(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class EstadoDeProblema(Enum):
    DETECTADO = "detectado"
    ANALIZANDOSE = "analizandose"
    ASIGNADO = "asignado"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"


class ProblemaForm(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    sintomas: str
    prioridad: PrioridadDeProblema
    categoria: str
    estado: EstadoDeProblema


class Problema(ProblemaForm, table=True):
    __tablename__ = "problemas"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_deteccion: datetime = Field(default=datetime.now())
