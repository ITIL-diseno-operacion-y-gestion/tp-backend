from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from .problema_incidente_link import ProblemaIncidenteLink
from .articulo_incidente_link import ArticuloIncidenteLink
from .error_conocido_incidente_link import ErrorConocidoIncidenteLink
from .articulo import Articulo
from api.enums.estado import Estado
from api.enums.categoria import Categoria
from api.enums.prioridad import Prioridad


class FormaDeNotificacion(Enum):
    LLAMADA_TELEFONICA = "llamada telefonica"
    EMAIL = "email"
    SMS = "sms"
    FORMULARIO_WEB = "formulario web"
    CHAT_EN_VIVO = "chat en vivo"


class IncidenteBase(SQLModel):
    id_usuario: int = Field(default=None, foreign_key="usuarios.id")
    nombre: str
    forma_de_notificacion: FormaDeNotificacion
    servicios_afectados: str
    prioridad: Prioridad
    categoria: Categoria
    informacion_adicional: str
    conformidad_resolucion: Optional[int] = Field(default=None, ge=1, le=10)
    id_agente_asignado: Optional[int] = Field(default=None, nullable=True)
    estado: Optional[Estado] = Field(default=None, nullable=True)


class IncidentePatchForm(SQLModel):
    estado: Optional[Estado] = Field(default=None, nullable=True)
    id_agente_asignado: Optional[int] = Field(default=None, nullable=True)
    conformidad_resolucion: Optional[int] = Field(default=None, ge=1, le=10)
    nombre: Optional[str] = Field(default=None)
    forma_de_notificacion: Optional[FormaDeNotificacion] = Field(default=None)
    servicios_afectados: Optional[str] = Field(default=None)
    prioridad: Optional[Prioridad] = Field(default=None)
    categoria: Optional[Categoria] = Field(default=None)
    informacion_adicional: Optional[str] = Field(default=None)


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
    conformidad_resolucion: Optional[int] = Field(default=None, ge=0, le=10)


class IncidentePublico(IncidenteBase):
    id: Optional[int]
    fecha_de_alta: datetime
    articulos_afectados: List[Articulo] = []
    conformidad_resolucion: Optional[int]
    nombre: Optional[str] = Field(default=None, nullable=True)
