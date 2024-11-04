from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import cast, Date
from ..db import get_session
from ..modelo.reporte import Reporte, ReporteArticulos, ReporteCambios, ReporteIncidentes, ReporteProblemas, ReporteErrores
from ..modelo.articulo import Articulo
from ..modelo.cambio import Cambio
from ..modelo.incidente import Incidente
from ..modelo.problema import Problema
from ..modelo.error_conocido import ErrorConocido
import secrets
import string
from typing import Optional
from datetime import date
from collections import Counter


router = APIRouter(
    prefix="/reportes",
    tags=["reportes"],
)

def crearReporteArticulos(desde, hasta, session):
    query = select(Articulo)
    if desde is not None:
        query = query.where(Articulo.fecha_de_alta >= desde)
    if hasta is not None:
        query = query.where(Articulo.fecha_de_alta <= hasta)
    articulos = session.exec(query).all()

    reporteArticulos = ReporteArticulos()
    reporteArticulos.tipo = Counter(articulo.tipo for articulo in articulos)
    reporteArticulos.estado = Counter(articulo.estado for articulo in articulos)
    return reporteArticulos


def crearReporteCambios(desde, hasta, session):
    query = select(Cambio)
    if desde is not None:
        query = query.where(Cambio.fecha_de_creacion >= desde)
    if hasta is not None:
        query = query.where(Cambio.fecha_de_creacion <= hasta)
    cambios = session.exec(query).all()

    reporteCambios = ReporteCambios()
    reporteCambios.estado = Counter(cambio.estado for cambio in cambios)
    reporteCambios.prioridad = Counter(cambio.prioridad for cambio in cambios)
    reporteCambios.categoria = Counter(cambio.categoria for cambio in cambios)
    reporteCambios.articulo = Counter(articulo.id for cambio in cambios for articulo in cambio.articulos_afectados)
    return reporteCambios

def crearReporteIncidentes(desde, hasta, session):
    query = select(Incidente)
    if desde is not None:
        query = query.where(Incidente.fecha_de_alta >= desde)
    if hasta is not None:
        query = query.where(Incidente.fecha_de_alta <= hasta)
    incidentes = session.exec(query).all()

    reporteIncidentes = ReporteIncidentes()
    reporteIncidentes.prioridad = Counter(incidente.prioridad for incidente in incidentes)
    reporteIncidentes.categoria = Counter(incidente.categoria for incidente in incidentes)
    reporteIncidentes.articulo = Counter(articulo.id for incidente in incidentes for articulo in incidente.articulos_afectados)
    return reporteIncidentes

def crearReporteProblemas(desde, hasta, session):
    query = select(Problema)
    if desde is not None:
        query = query.where(cast(Problema.fecha_de_deteccion, Date) >= desde)
    if hasta is not None:
        query = query.where(cast(Problema.fecha_de_deteccion, Date) <= hasta)
    problemas = session.exec(query).all()

    reporteProblemas = ReporteProblemas()
    reporteProblemas.categoria = Counter(problema.categoria for problema in problemas)
    reporteProblemas.estado = Counter(problema.estado for problema in problemas)
    reporteProblemas.incidente = Counter(incidente.id for problema in problemas for incidente in problema.incidentes)
    return reporteProblemas

def crearReporteErrores(desde, hasta, session):
    query = select(ErrorConocido)
    if desde is not None:
        query = query.where(ErrorConocido.fecha_de_creacion >= desde)
    if hasta is not None:
        query = query.where(ErrorConocido.fecha_de_creacion <= hasta)
    errores = session.exec(query).all()

    reporteErrores = ReporteErrores()
    reporteErrores.incidente = Counter(incidente.id for error in errores for incidente in error.incidentes)
    reporteErrores.problema = Counter(problema.id for error in errores for problema in error.problemas)
    return reporteErrores


@router.get("")
def obtener_reporte(
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
    session: Session = Depends(get_session)
):
    reporte = Reporte()

    reporte.articulos = crearReporteArticulos(desde, hasta, session)

    reporte.cambios = crearReporteCambios(desde, hasta, session)

    reporte.incidentes = crearReporteIncidentes(desde, hasta, session)

    reporte.problemas = crearReporteProblemas(desde, hasta, session)

    reporte.errores = crearReporteErrores(desde, hasta, session)

    return reporte

