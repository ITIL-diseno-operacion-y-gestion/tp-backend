from typing import Optional
from sqlmodel import SQLModel, Field


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    fecha_de_alta: str
    forma_de_notificacion: str
    reportador: str
    usuarios_afectados: str
    servicios_afectados: str
    prioridad: str
    categoria: str
    informacion_adicional: str
