from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ArticuloUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    titular: str | None = None
    tipo: str | None = None
    info_fabricacion: str | None = None
    version: int | None = None
    localizacion: str | None = None
    relacion_items: str | None = None


class ArticuloForm(SQLModel):
    nombre: str
    descripcion: str
    titular: str
    tipo: str
    info_fabricacion: str
    version: int
    localizacion: str
    relacion_items: str


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
    fecha_de_alta: datetime = Field(default=datetime.now())
    relacion_items: str
    esta_activo: bool = Field(default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "titular": self.titular,
            "tipo": self.tipo,
            "info_fabricacion": self.info_fabricacion,
            "version": self.version,
            "localizacion": self.localizacion,
            "fecha_de_alta": self.fecha_de_alta,
        }
