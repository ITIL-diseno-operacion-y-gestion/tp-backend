from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from .articulo_incidente_link import ArticuloIncidenteLink
from .articulo_cambio_link import ArticuloCambioLink
from pydantic import BaseModel
from typing import Dict

class ReporteArticulos(BaseModel):
    tipo: Optional[Dict[str, int]] = Field(default=None)
    estado: Optional[Dict[str, int]] = Field(default=None)

class ReporteCambios(BaseModel):
    estado: Optional[Dict[str, int]] = Field(default=None)
    prioridad: Optional[Dict[str, int]] = Field(default=None)
    categoria: Optional[Dict[str, int]] = Field(default=None)
    articulo: Optional[Dict[str, int]] = Field(default=None)

class ReporteIncidentes(BaseModel):
    prioridad: Optional[Dict[str, int]] = Field(default=None)
    categoria: Optional[Dict[str, int]] = Field(default=None)
    articulo: Optional[Dict[str, int]] = Field(default=None)

class ReporteProblemas(BaseModel):
    categoria: Optional[Dict[str, int]] = Field(default=None)
    estado: Optional[Dict[str, int]] = Field(default=None)
    incidente: Optional[Dict[str, int]] = Field(default=None)

class ReporteErrores(BaseModel):
    incidente: Optional[Dict[str, int]] = Field(default=None)
    problema: Optional[Dict[str, int]] = Field(default=None)



class Reporte(BaseModel):
    articulos: Optional[ReporteArticulos] = Field(default=None)
    cambios: Optional[ReporteCambios] = Field(default=None)
    incidentes: Optional[ReporteIncidentes] = Field(default=None)
    problemas: Optional[ReporteProblemas] = Field(default=None)
    errores: Optional[ReporteErrores] = Field(default=None)
