from typing import Optional
from sqlmodel import SQLModel, Field


class Articulo(SQLModel, table=True):
    __tablename__ = "articulos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    titular: str
    tipo: str
    info_fabricacion: str
    version: int
    localizacion: str
    fecha_de_alta: str
    relacion_items: str
    esta_activo: bool