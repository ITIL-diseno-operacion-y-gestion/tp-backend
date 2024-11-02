from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from .error_conocido_incidente_link import ErrorConocidoIncidenteLink
from .error_conocido_problema_link import ErrorConocidoProblemaLink
from .incidente import Incidente
from .problema import Problema


class ErrorConocidoBase(SQLModel):
    descripcion: str
    sintomas: str
    solucion_definitiva: str
    solucion_provisoria: str


class ErrorConocidoForm(ErrorConocidoBase):
    ids_incidentes: List[int]
    ids_problemas: List[int]


class ErrorConocido(ErrorConocidoBase, table=True):
    __tablename__ = "errores_conocidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_creacion: Optional[datetime] = Field(default=None)
    incidentes: List["Incidente"] = Relationship(
        back_populates="errores_conocidos", link_model=ErrorConocidoIncidenteLink
    )
    problemas: List["Problema"] = Relationship(
        back_populates="errores_conocidos", link_model=ErrorConocidoProblemaLink
    )


class ErrorConocidoPublico(ErrorConocidoBase):
    id: Optional[int]
    fecha_de_creacion: datetime
    incidentes: List[Incidente] = []
    problemas: List[Problema] = []
