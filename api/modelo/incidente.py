from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class IncidenteForm(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    forma_de_notificacion: str
    reportador: str
    usuarios_afectados: str
    servicios_afectados: str
    prioridad: str
    categoria: str
    informacion_adicional: str

class Incidente(IncidenteForm, table=True):
    __tablename__ = "incidentes"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_alta: datetime = Field(default=datetime.now())
