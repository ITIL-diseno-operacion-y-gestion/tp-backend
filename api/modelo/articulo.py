from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class TipoDeArticulo(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    DOCUMENTACION = "documentacion"
    INSTALACION = "instalacion"
    PROVEEDOR = "proveedor"
    SERVICIO_TECNICO = "servicio tecnico"


class ArticuloForm(SQLModel):
    nombre: str
    descripcion: str
    titular: str
    tipo: TipoDeArticulo
    info_fabricacion: str
    version: Optional[int]
    localizacion: str
    relacion_items: str


class Articulo(ArticuloForm, table=True):
    __tablename__ = "articulos"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_alta: datetime = Field(default=datetime.now())
    esta_activo: bool = Field(default=True)
