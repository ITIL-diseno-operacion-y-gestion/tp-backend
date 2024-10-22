from typing import Optional
from sqlmodel import SQLModel, Field


class ArticuloIncidenteLink(SQLModel, table=True):
    __tablename__ = "articulos_incidentes"

    id_articulo: Optional[int] = Field(
        default=None, foreign_key="articulos.id", primary_key=True
    )
    id_incidente: Optional[int] = Field(
        default=None, foreign_key="incidentes.id", primary_key=True
    )
