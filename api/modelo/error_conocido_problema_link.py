from typing import Optional
from sqlmodel import SQLModel, Field


class ErrorConocidoProblemaLink(SQLModel, table=True):
    __tablename__ = "errores_conocidos_problemas"

    id_error_conocido: Optional[int] = Field(
        default=None, foreign_key="errores_conocidos.id", primary_key=True
    )
    id_problema: Optional[int] = Field(
        default=None, foreign_key="problemas.id", primary_key=True
    )
