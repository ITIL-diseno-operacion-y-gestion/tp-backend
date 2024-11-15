from typing import Optional
from sqlmodel import SQLModel, Field, JSON, Column
from pydantic import BaseModel
from datetime import datetime

ACCION_CREACION = "creacion"
ACCION_ACTUALIZACION = "actualizacion"
ACCION_ELIMINACION = "eliminacion"

def registrar_accion(session, clase_entidad_, id_entidad_, accion_, estado_anterior_, estado_nuevo_):
    auditoria = Auditoria(
        clase_entidad = clase_entidad_,
        id_entidad = id_entidad_,
        accion = accion_,
        fecha_de_accion = datetime.now(),
        estado_anterior = estado_anterior_,
        estado_nuevo = estado_nuevo_
    )
    print("por crear audit: ", auditoria)
    session.add(auditoria)
    session.commit()
    session.refresh(auditoria)
    print("creè audit: ", auditoria)


class AuditoriaBase(SQLModel):
    clase_entidad: Optional[str] = Field(default=None)
    id_entidad: Optional[str] = Field(default=None)
    fecha_de_accion: Optional[datetime] = Field(default=None)
    accion: Optional[str] = Field(default=None)
    estado_anterior: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    estado_nuevo: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Auditoria(AuditoriaBase, table=True):
    __tablename__ = "auditorias"

    id: Optional[int] = Field(default=None, primary_key=True)
