from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from .problema_incidente_link import ProblemaIncidenteLink
from .articulo_incidente_link import ArticuloIncidenteLink
from .error_conocido_incidente_link import ErrorConocidoIncidenteLink
from .articulo import Articulo


class FormaDeNotificacion(Enum):
    LLAMADA_TELEFONICA = "llamada telefonica"
    EMAIL = "email"
    SMS = "sms"
    FORMULARIO_WEB = "formulario web"
    CHAT_EN_VIVO = "chat en vivo"


class Prioridad(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class Categoria(Enum):
    DE_SEGURIDAD = "de seguridad"
    TECNICO = "tecnico"
    DE_DISPONIBILIDAD = "de disponibilidad"
    DE_DATOS = "de datos"
    LEGAL = "legal"


class IncidenteBase(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    forma_de_notificacion: FormaDeNotificacion
    reportador: str
    usuarios_afectados: str
    servicios_afectados: str
    prioridad: Prioridad
    categoria: Categoria
    informacion_adicional: str


class IncidenteForm(IncidenteBase):
    ids_articulos: List[int]


class Incidente(IncidenteBase, table=True):
    __tablename__ = "incidentes"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_de_alta: Optional[datetime] = Field(default=None)
    problemas: List["Problema"] = Relationship(
        back_populates="incidentes", link_model=ProblemaIncidenteLink
    )
    articulos_afectados: List[Articulo] = Relationship(
        back_populates="incidentes_relacionados", link_model=ArticuloIncidenteLink
    )
    errores_conocidos: List["ErrorConocido"] = Relationship(
        back_populates="incidentes", link_model=ErrorConocidoIncidenteLink
    )


class IncidentePublico(IncidenteBase):
    id: Optional[int]
    fecha_de_alta: datetime
    articulos_afectados: List[Articulo] = []
