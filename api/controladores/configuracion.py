from fastapi import APIRouter, Depends

from sqlmodel import Session, select
from ..db import get_session, obtener_por_id
from ..modelo.articulo import Articulo, ArticuloForm
from ..modelo.usuario import Usuario
from datetime import datetime

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
)


@router.get("/articulos/{id}")
def obtener_articulo_por_id(id, session: Session = Depends(get_session)):
    return obtener_por_id(Articulo, id, session)


@router.get("/articulos")
def obtener_articulos(
    nombre: str | None = None, session: Session = Depends(get_session)
):
    query = select(Articulo).where(Articulo.esta_activo == True)
    if nombre:
        query = query.where(Articulo.nombre == nombre)
    articulos = session.exec(query).all()
    return articulos


@router.post("/articulos")
def crear_articulo(
    articulo_form: ArticuloForm, session: Session = Depends(get_session)
):
    usuario = obtener_por_id(Usuario, articulo_form.id_titular, session)
    articulo = Articulo.model_validate(articulo_form)
    articulo.fecha_de_alta = datetime.now()
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    return articulo


@router.delete("/articulos/{id}")
def dar_de_baja_articulo_por_id(id, session: Session = Depends(get_session)):
    articulo = obtener_por_id(Articulo, id, session)
    articulo.esta_activo = False
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    return articulo


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
