from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from .articulo_incidente_link import ArticuloIncidenteLink
from .articulo_cambio_link import ArticuloCambioLink
from pydantic import BaseModel
from typing import Dict
from datetime import datetime, timedelta

class ReporteArticulos(BaseModel):
    tipo: Optional[Dict[str, int]] = Field(default={})
    estado: Optional[Dict[str, int]] = Field(default={})
    total: Optional[int] = Field(default=0)

class ReporteCambios(BaseModel):
    estado: Optional[Dict[str, int]] = Field(default={})
    prioridad: Optional[Dict[str, int]] = Field(default={})
    categoria: Optional[Dict[str, int]] = Field(default={})
    articulo: Optional[Dict[str, int]] = Field(default={})
    total: Optional[int] = Field(default=0)

class ReporteIncidentes(BaseModel):
    prioridad: Optional[Dict[str, int]] = Field(default={})
    categoria: Optional[Dict[str, int]] = Field(default={})
    articulo: Optional[Dict[str, int]] = Field(default={})
    conformidad_resolucion_promedio: Optional[int] = Field(default=0)
    total: Optional[int] = Field(default=0)

class ReportesIncidentes(BaseModel):
    generales: Optional[ReporteIncidentes] = Field(default=ReporteIncidentes)
    personales: Optional[ReporteIncidentes] = Field(default=ReporteIncidentes)

class ReporteProblemas(BaseModel):
    categoria: Optional[Dict[str, int]] = Field(default={})
    estado: Optional[Dict[str, int]] = Field(default={})
    incidente: Optional[Dict[str, int]] = Field(default={})
    total: Optional[int] = Field(default=0)
    tiempo_promedio_resolucion: Optional[str] = Field(default="")

class ReportesProblemas(BaseModel):
    generales: Optional[ReporteProblemas] = Field(default=ReporteProblemas)
    personales: Optional[ReporteProblemas] = Field(default=ReporteProblemas)

class ReporteErrores(BaseModel):
    incidente: Optional[Dict[str, int]] = Field(default={})
    problema: Optional[Dict[str, int]] = Field(default={})
    total: Optional[int] = Field(default=0)


class Reporte(BaseModel):
    articulos: Optional[ReporteArticulos] = Field(default=None)
    cambios: Optional[ReporteCambios] = Field(default=None)
    incidentes: Optional[ReportesIncidentes] = Field(default=None)
    problemas: Optional[ReportesProblemas] = Field(default=None)
    errores: Optional[ReporteErrores] = Field(default=None)
