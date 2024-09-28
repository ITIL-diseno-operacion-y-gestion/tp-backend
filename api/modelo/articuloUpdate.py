from sqlmodel import SQLModel


class ArticuloUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    titular: str | None = None
    tipo: str | None = None
    info_fabricacion: str | None = None
    version: int | None = None
    localizacion: str | None = None
    relacion_items: str | None = None
