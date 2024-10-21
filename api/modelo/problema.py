from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from .problema_incidente_link import ProblemaIncidenteLink
from .incidente import Incidente


class Prioridad(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class Estado(Enum):
    DETECTADO = "detectado"
    ANALIZANDOSE = "analizandose"
    ASIGNADO = "asignado"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"


class Categoria(Enum):
    DE_SEGURIDAD = "de seguridad"
    TECNICO = "tecnico"
    DE_DISPONIBILIDAD = "de disponibilidad"
    DE_DATOS = "de datos"
    LEGAL = "legal"


class ProblemaBase(SQLModel):
    sintomas: str
    prioridad: Prioridad
    categoria: Categoria
    estado: Estado


class ProblemaForm(ProblemaBase):
    ids_incidentes: List[int]


class Problema(ProblemaBase, table=True):
    __tablename__ = "problemas"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_deteccion: datetime = Field(default=datetime.now())
    incidentes: List[Incidente] = Relationship(
        back_populates="problemas", link_model=ProblemaIncidenteLink
    )


class ProblemaPublico(ProblemaBase):
    id: Optional[int]
    fecha_de_deteccion: datetime
    incidentes: List[Incidente] = []

class ProblemaUpdateForm(BaseModel):
    sintomas: Optional[str] = None
    prioridad: Optional[Prioridad] = None
    categoria: Optional[Categoria] = None
    estado: Optional[Estado] = None