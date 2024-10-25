from typing import Optional
from sqlmodel import SQLModel, Field


class ArticuloCambioLink(SQLModel, table=True):
    __tablename__ = "articulos_cambios"

    id_articulo: Optional[int] = Field(
        default=None, foreign_key="articulos.id", primary_key=True
    )
    id_cambio: Optional[int] = Field(
        default=None, foreign_key="cambios.id", primary_key=True
    )
