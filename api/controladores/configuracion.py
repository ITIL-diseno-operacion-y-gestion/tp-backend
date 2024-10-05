from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from sqlmodel import Session, select
from ..db import get_session
from ..modelo.articulo import Articulo

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
)


@router.get("/articulos/{id}")
def obtener_articulo_por_id(id, session: Session = Depends(get_session)):
    articulo = session.exec(
        select(Articulo).where(Articulo.id == id).where(Articulo.esta_activo == True)
    ).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo not found")
    return articulo


@router.get("/articulos")
def obtener_articulos(
    nombre: str | None = None, session: Session = Depends(get_session)
):
    if nombre:
        print("nombre: ", nombre)
        return session.exec(
            select(Articulo)
            .where(Articulo.nombre == nombre)
            .where(Articulo.esta_activo == True)
        ).all()
    else:
        print("nombre null")
        return session.exec(select(Articulo).where(Articulo.esta_activo == True)).all()


# def registrar_modificacion(articulo_orig, articulo, accion, session):
#     audit = Audit()
#     audit.id_articulo = articulo.id
#     audit.fecha = datetime.now()
#     audit.accion = accion
#     if articulo_orig is not None:
#         audit.estado_anterior = articulo_orig.to_dict()
#     audit.estado_nuevo = articulo.to_dict()
#     print("audit: ", audit)
#     #session.add(audit)
#     #session.commit()

# @router.patch("/articulos/{id}")
# def actualizar_articulo(
#     id, articuloUpdate: ArticuloUpdate, session: Session = Depends(get_session)
# ):
#     articuloDb = session.exec(select(Articulo).where(Articulo.id == id)).first()
#     articulo_orig = articuloDb
#     if not articuloDb:
#         raise HTTPException(status_code=404, detail="Articulo not found")
#     articuloData = articuloUpdate.model_dump(exclude_unset=True)
#     articuloDb.sqlmodel_update(articuloData)
#     session.add(articuloDb)
#     session.commit()
#     session.refresh(articuloDb)
#     registrar_modificacion(articulo_orig, articuloDb, "modificacion", session)
#     return articuloDb


@router.post("/articulos")
def crear_articulo(articulo: Articulo, session: Session = Depends(get_session)):
    articulo.id = None
    articulo.esta_activo = True
    articulo.fecha_de_alta = datetime.now()
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    # registrar_modificacion(None, articulo, "creacion", session)
    return articulo


@router.delete("/articulos/{id}")
def dar_de_baja_articulo(id, session: Session = Depends(get_session)):
    articulo = session.exec(select(Articulo).where(Articulo.id == id)).first()
    articulo_orig = articulo
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo not found")
    articulo.esta_activo = False
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    registrar_modificacion(articulo_orig, articulo, "borrado", session)
    return articulo
