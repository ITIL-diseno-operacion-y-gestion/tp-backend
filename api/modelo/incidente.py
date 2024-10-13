from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Incidente(SQLModel, table=True):
    __tablename__ = "incidentes"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    fecha_de_alta: datetime = Field(default=datetime.now())
    forma_de_notificacion: str
    reportador: str
    usuarios_afectados: str
    servicios_afectados: str
    prioridad: str
    categoria: str
    informacion_adicional: str
