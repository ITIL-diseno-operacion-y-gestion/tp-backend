from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy import cast, Date
from ..db import get_session
from ..modelo.reporte import (
    Reporte,
    ReporteArticulos,
    ReporteCambios,
    ReporteIncidentes,
    ReportesProblemas,
    ReporteProblemas,
    ReporteErrores,
    ReportesIncidentes,
)
from ..modelo.articulo import Articulo
from ..modelo.cambio import Cambio
from ..modelo.incidente import Incidente
from ..modelo.problema import Problema
from ..modelo.problema_incidente_link import ProblemaIncidenteLink
from ..modelo.error_conocido import ErrorConocido
from typing import Optional
from datetime import date, datetime, timedelta
from collections import Counter


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
)


def crear_reporte_articulos(desde, hasta, session):
    query = select(Articulo)
    if desde is not None:
        query = query.where(Articulo.fecha_de_alta >= desde)
    if hasta is not None:
        query = query.where(Articulo.fecha_de_alta <= hasta)
    articulos = session.exec(query).all()

    reporte_articulos = ReporteArticulos()
    reporte_articulos.tipo = Counter(articulo.tipo for articulo in articulos)
    reporte_articulos.estado = Counter(articulo.estado for articulo in articulos)
    reporte_articulos.total = len(articulos)
    return reporte_articulos


def crear_reporte_cambios(desde, hasta, session):
    query = select(Cambio)
    if desde is not None:
        query = query.where(Cambio.fecha_de_creacion >= desde)
    if hasta is not None:
        query = query.where(Cambio.fecha_de_creacion <= hasta)
    cambios = session.exec(query).all()

    reporte_cambios = ReporteCambios()
    reporte_cambios.estado = Counter(cambio.estado for cambio in cambios)
    reporte_cambios.prioridad = Counter(cambio.prioridad for cambio in cambios)
    reporte_cambios.categoria = Counter(cambio.categoria for cambio in cambios)
    reporte_cambios.articulo = Counter(
        articulo.id for cambio in cambios for articulo in cambio.articulos_afectados
    )
    reporte_cambios.total = len(cambios)
    return reporte_cambios


def obtener_conformidad_resolucion_promedio(incidentes):
    valores_conformidad = []
    for incidente in incidentes:
        if incidente.conformidad_resolucion is not None:
            valores_conformidad.append(int(incidente.conformidad_resolucion))
    print("valores_conformidad: ", valores_conformidad)
    if len(valores_conformidad) > 0:
        return sum(valores_conformidad) / len(valores_conformidad)
    return 0


def crear_reporte_incidentes(id_agente_asignado, desde, hasta, session):
    query = select(Incidente)
    if desde is not None:
        query = query.where(Incidente.fecha_de_alta >= desde)
    if hasta is not None:
        query = query.where(Incidente.fecha_de_alta <= hasta)
    if id_agente_asignado is not None:
        query = query.where(Incidente.id_agente_asignado == id_agente_asignado)
    incidentes = session.exec(query).all()

    reporte_incidentes = ReporteIncidentes()
    reporte_incidentes.prioridad = Counter(
        incidente.prioridad for incidente in incidentes
    )
    reporte_incidentes.categoria = Counter(
        incidente.categoria for incidente in incidentes
    )
    reporte_incidentes.articulo = Counter(
        articulo.id
        for incidente in incidentes
        for articulo in incidente.articulos_afectados
    )
    reporte_incidentes.conformidad_resolucion_promedio = (
        obtener_conformidad_resolucion_promedio(incidentes)
    )
    reporte_incidentes.total = len(incidentes)
    return reporte_incidentes


FORMATO_FECHA = "%Y-%m-%d %H:%M:%S.%f"


def obtener_tiempos_de_resolucion(problemas):
    tiempos_de_resolucion = []
    print("empiezo analisis")
    for problema in problemas:
        print("analizo problema pendiente: ", problema)
        if problema.fecha_de_resolucion is not None:
            print("analizo problema resuelto: ", problema)
            fecha_de_resolucion = datetime.strptime(
                problema.fecha_de_resolucion, FORMATO_FECHA
            )
            fecha_de_deteccion = datetime.strptime(
                problema.fecha_de_deteccion, FORMATO_FECHA
            )
            tiempos_de_resolucion.append(fecha_de_resolucion - fecha_de_deteccion)
    return tiempos_de_resolucion


def formatear_tiempo_promedio_de_resolucion(tiempo_promedio_resolucion):
    dias = tiempo_promedio_resolucion.days
    segundos_totales = tiempo_promedio_resolucion.seconds
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60
    return f"{dias} d, {horas:02}:{minutos:02}:{segundos:02}"


def obtener_tiempo_promedio_de_resolucion(problemas):
    tiempos_de_resolucion = obtener_tiempos_de_resolucion(problemas)

    if len(tiempos_de_resolucion) > 0:
        tiempo_promedio_de_resolucion = sum(tiempos_de_resolucion, timedelta()) / len(
            tiempos_de_resolucion
        )
        return formatear_tiempo_promedio_de_resolucion(tiempo_promedio_de_resolucion)
    return ""


def crear_reporte_problemas(id_agente_asignado, desde, hasta, session):
    query = select(Problema)
    if desde is not None:
        query = query.where(cast(Problema.fecha_de_deteccion, Date) >= desde)
    if hasta is not None:
        query = query.where(cast(Problema.fecha_de_deteccion, Date) <= hasta)
    if id_agente_asignado is not None:
        query = (
            query.join(ProblemaIncidenteLink)
            .join(Incidente)
            .where(Incidente.id_agente_asignado == id_agente_asignado)
        )
    problemas = session.exec(query).all()
    reporte_problemas = ReporteProblemas()
    reporte_problemas.categoria = Counter(problema.categoria for problema in problemas)
    reporte_problemas.estado = Counter(problema.estado for problema in problemas)
    reporte_problemas.incidente = Counter(
        incidente.id for problema in problemas for incidente in problema.incidentes
    )

    reporte_problemas.tiempo_promedio_resolucion = (
        obtener_tiempo_promedio_de_resolucion(problemas)
    )
    print(
        "reporte_problemas.tiempo_promedio_resolucion: ",
        reporte_problemas.tiempo_promedio_resolucion,
    )
    reporte_problemas.total = len(problemas)

    return reporte_problemas


def crear_reporte_errores(desde, hasta, session):
    query = select(ErrorConocido)
    if desde is not None:
        query = query.where(ErrorConocido.fecha_de_creacion >= desde)
    if hasta is not None:
        query = query.where(ErrorConocido.fecha_de_creacion <= hasta)
    errores = session.exec(query).all()

    reporte_errores = ReporteErrores()
    reporte_errores.incidente = Counter(
        incidente.id for error in errores for incidente in error.incidentes
    )
    reporte_errores.problema = Counter(
        problema.id for error in errores for problema in error.problemas
    )
    reporte_errores.total = len(errores)
    return reporte_errores


@router.get("")
def obtener_reporte(
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
    id_agente_asignado: Optional[int] = None,
    session: Session = Depends(get_session),
):
    reporte = Reporte()
    reporte.articulos = crear_reporte_articulos(desde, hasta, session)
    reporte.cambios = crear_reporte_cambios(desde, hasta, session)
    reporte.incidentes = ReportesIncidentes()
    reporte.problemas = ReportesProblemas()
    reporte.incidentes.generales = crear_reporte_incidentes(None, desde, hasta, session)
    reporte.problemas.generales = crear_reporte_problemas(None, desde, hasta, session)

    if id_agente_asignado:
        reporte.incidentes.personales = crear_reporte_incidentes(
            id_agente_asignado, desde, hasta, session
        )
        reporte.problemas.personales = crear_reporte_problemas(
            id_agente_asignado, desde, hasta, session
        )
    else:
        reporte_incidentes_personales = ReporteIncidentes()
        reporte.incidentes.personales = reporte_incidentes_personales

        reporte_problemas_personales = ReporteProblemas()
        reporte.problemas.personales = reporte_problemas_personales

    reporte.errores = crear_reporte_errores(desde, hasta, session)
    return reporte
