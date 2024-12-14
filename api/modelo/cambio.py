from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import NonNegativeFloat
from .articulo_cambio_link import ArticuloCambioLink
from .articulo import Articulo


class Estado(Enum):
    CREADO = "creado"
    RECIBIDO = "recibido"
    ACEPTADO = "aceptado"
    RECHAZADO = "rechazado"
    EN_PROGRESO = "en progreso"
    APLICADO = "aplicado"


class Prioridad(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class Categoria(Enum):
    DE_SEGURIDAD = "de seguridad"
    TECNICO = "tecnico"
    DE_DISPONIBILIDAD = "de disponibilidad"
    DE_DATOS = "de datos"
    LEGAL = "legal"


class Impacto(Enum):
    MENOR = "menor"
    SIGNIFICATIVO = "significativo"
    MAYOR = "mayor"


class CambioBase(SQLModel):
    id_solicitante: int = Field(default=None, foreign_key="usuarios.id")
    nombre: str
    estado: Estado
    motivo_de_implementacion: str
    descripcion: str
    prioridad: Prioridad
    categoria: Categoria
    impacto: Impacto
    fecha_de_implementacion: datetime
    horas_necesarias: NonNegativeFloat
    costo_estimado: NonNegativeFloat
    riesgos_asociados: str


class CambioForm(CambioBase):
    ids_articulos: List[int]


class Cambio(CambioBase, table=True):
    __tablename__ = "cambios"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_creacion: Optional[datetime] = Field(default=None)
    articulos_afectados: List[Articulo] = Relationship(
        back_populates="cambios_relacionados", link_model=ArticuloCambioLink
    )


class CambioPublico(CambioBase):
    id: int
    nombre: Optional[str]
    fecha_de_creacion: datetime
    articulos_afectados: List[Articulo] = []


class CambioUpdateForm(SQLModel):
    nombre: Optional[str] = None
    estado: Optional[Estado] = None
    motivo_de_implementacion: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[Prioridad] = None
    categoria: Optional[Categoria] = None
    impacto: Optional[Impacto] = None
    fecha_de_implementacion: Optional[datetime] = None
    horas_necesarias: Optional[NonNegativeFloat] = None
    costo_estimado: Optional[NonNegativeFloat] = None
    riesgos_asociados: Optional[str] = None
