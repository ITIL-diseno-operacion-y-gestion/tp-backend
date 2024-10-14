from typing import Optional
from sqlmodel import SQLModel, Field  # , Relationship
from enum import Enum
from datetime import datetime
# from .incidente import Incidente


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


class CategoriaDeProblema(Enum):
    DE_SEGURIDAD = "de seguridad"
    TECNICO = "tecnico"
    DE_DISPONIBILIDAD = "de disponibilidad"
    DE_DATOS = "de datos"
    LEGAL = "legal"


class ProblemaForm(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    sintomas: str
    prioridad: PrioridadDeProblema
    categoria: CategoriaDeProblema
    estado: EstadoDeProblema


# class ProblemaIncidenteLink(SQLModel, table=True):
#     __tablename__ = "problemas_incidentes"

#     id_problema: Optional[int] = Field(
#         default=None, foreign_key="problemas.id", primary_key=True
#     )
#     id_incidente: Optional[int] = Field(
#         default=None, foreign_key="incidentes.id", primary_key=True
#     )


class Problema(ProblemaForm, table=True):
    __tablename__ = "problemas"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_deteccion: datetime = Field(default=datetime.now())
    # incidentes: list[Incidente] = Relationship(link_model=ProblemaIncidenteLink)
