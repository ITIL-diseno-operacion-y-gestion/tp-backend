from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime
from .problema_incidente_link import ProblemaIncidenteLink
from .error_conocido_problema_link import ErrorConocidoProblemaLink
from .incidente import Incidente
from api.enums.estado import Estado
from api.enums.categoria import Categoria
from api.enums.prioridad import Prioridad


class ProblemaBase(SQLModel):
    sintomas: str
    nombre: str
    prioridad: Prioridad
    categoria: Categoria
    estado: Estado


class ProblemaForm(ProblemaBase):
    ids_incidentes: List[int]


class Problema(ProblemaBase, table=True):
    __tablename__ = "problemas"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_deteccion: Optional[datetime] = Field(default=None)
    fecha_de_resolucion: Optional[datetime] = Field(default=None)
    incidentes: List[Incidente] = Relationship(
        back_populates="problemas", link_model=ProblemaIncidenteLink
    )
    errores_conocidos: List["ErrorConocido"] = Relationship(
        back_populates="problemas", link_model=ErrorConocidoProblemaLink
    )


class ProblemaPublico(ProblemaBase):
    id: Optional[int]
    nombre: Optional[str]
    fecha_de_deteccion: datetime
    incidentes: List[Incidente] = []


class ProblemaUpdateForm(BaseModel):
    sintomas: Optional[str] = None
    nombre: Optional[str] = None
    prioridad: Optional[Prioridad] = None
    categoria: Optional[Categoria] = None
    estado: Optional[Estado] = None
    ids_incidentes: List[int] = None
