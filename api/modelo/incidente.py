from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class FormaDeNotificacionDeIncidente(Enum):
    LLAMADA_TELEFONICA = "llamada telefonica"
    EMAIL = "email"
    SMS = "sms"
    FORMULARIO_WEB = "formulario web"
    CHAT_EN_VIVO = "chat en vivo"

class PrioridadDeIncidente(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class CategoriaDeIncidente(Enum):
    DE_SEGURIDAD = "de seguridad"
    TECNICO = "tecnico"
    DE_DISPONIBILIDAD = "de disponibilidad"
    DE_DATOS = "de datos"
    LEGAL = "legal"

class IncidenteForm(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    forma_de_notificacion: FormaDeNotificacionDeIncidente
    reportador: str
    usuarios_afectados: str
    servicios_afectados: str
    prioridad: PrioridadDeIncidente
    categoria: CategoriaDeIncidente
    informacion_adicional: str

class Incidente(IncidenteForm, table=True):
    __tablename__ = "incidentes"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_alta: datetime = Field(default=datetime.now())
