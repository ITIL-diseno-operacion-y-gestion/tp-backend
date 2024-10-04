from typing import Optional
from sqlmodel import SQLModel, Field


class Audit(SQLModel, table=True):
    __tablename__ = "auditorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_articulo: int
    fecha: str
    accion: str
    campo_alterado: str
    estado_anterior: str
    estado_nuevo: str
