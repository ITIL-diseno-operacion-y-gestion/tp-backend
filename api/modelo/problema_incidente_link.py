from typing import Optional
from sqlmodel import SQLModel, Field


class ProblemaIncidenteLink(SQLModel, table=True):
    __tablename__ = "problemas_incidentes"

    id_problema: Optional[int] = Field(
        default=None, foreign_key="problemas.id", primary_key=True
    )
    id_incidente: Optional[int] = Field(
        default=None, foreign_key="incidentes.id", primary_key=True
    )
