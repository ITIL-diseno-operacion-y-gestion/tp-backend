from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session, select
from ..db import get_session
from ..modelo.articulo import Articulo, ArticuloForm

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
)


@router.get("/articulos/{id}")
def obtener_articulo_por_id(id, session: Session = Depends(get_session)):
    articulo = session.get_one(Articulo, id)
    return articulo


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
    articulo = Articulo.model_validate(articulo_form)
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    # registrar_modificacion(None, articulo, "creacion", session)
    return articulo


@router.delete("/articulos/{id}")
def dar_de_baja_articulo_por_id(id, session: Session = Depends(get_session)):
    articulo = session.exec(select(Articulo).where(Articulo.id == id)).first()
    if not articulo:
        raise HTTPException(
            status_code=404, detail=f"Articulo con id {id} no encontrado"
        )
    articulo.esta_activo = False
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    # registrar_modificacion(articulo_orig, articulo, "borrado", session)
    return articulo


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
