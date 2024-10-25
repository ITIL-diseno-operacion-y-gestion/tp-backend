from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from .articulo_incidente_link import ArticuloIncidenteLink
from .articulo_cambio_link import ArticuloCambioLink


class Tipo(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    DOCUMENTACION = "documentacion"
    INSTALACION = "instalacion"
    PROVEEDOR = "proveedor"
    SERVICIO_TECNICO = "servicio tecnico"


class Estado(Enum):
    PLANEADO = "planeado"
    ENCARGADO = "encargado"
    EN_CREACION = "en creacion"
    EN_PRUEBA = "en prueba"
    EN_ALMACEN = "en almacen"
    EN_PRODUCCION = "en produccion"
    EN_MANTENIMIENTO = "en mantenimiento"


class ArticuloForm(SQLModel):
    nombre: str
    descripcion: str
    id_titular: int = Field(default=None, foreign_key="usuarios.id")
    tipo: Tipo
    info_fabricacion: str
    version: Optional[float] = Field(default=None, nullable=True)
    localizacion: str
    relacion_items: str
    estado: Estado


class Articulo(ArticuloForm, table=True):
    __tablename__ = "articulos"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_alta: datetime = Field(default=datetime.now())
    esta_activo: bool = Field(default=True)
    incidentes_relacionados: List["Incidente"] = Relationship(
        back_populates="articulos_afectados", link_model=ArticuloIncidenteLink
    )
    cambios_relacionados: List["Cambio"] = Relationship(
        back_populates="articulos_afectados", link_model=ArticuloCambioLink
    )
