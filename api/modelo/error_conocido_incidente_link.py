from typing import Optional
from sqlmodel import SQLModel, Field


class ErrorConocidoIncidenteLink(SQLModel, table=True):
    __tablename__ = "errores_conocidos_incidentes"

    id_error_conocido: Optional[int] = Field(
        default=None, foreign_key="errores_conocidos.id", primary_key=True
    )
    id_incidente: Optional[int] = Field(
        default=None, foreign_key="incidentes.id", primary_key=True
    )
