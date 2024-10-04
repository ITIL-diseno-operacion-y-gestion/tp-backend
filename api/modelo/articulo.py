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