from enum import Enum


class Estado(Enum):
    DETECTADO = "detectado"
    ANALIZANDOSE = "analizandose"
    ASIGNADO = "asignado"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"
