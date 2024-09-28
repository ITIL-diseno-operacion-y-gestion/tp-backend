from fastapi import APIRouter, Depends
from sqlmodel import Session, select, update
from ..db import get_session
from ..modelo.articulo import Articulo
from ..modelo.articuloUpdate import ArticuloUpdate

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
)

@router.get("/articulo/{id}")
def obtener_articulos(id, session: Session = Depends(get_session)):
    articulos = session.exec(select(Articulo).where(Articulo.id==id).where(Articulo.esta_activo==True)).first()
    return articulos

@router.get("/articulos")
def obtener_articulos(nombre: str | None = None, session: Session = Depends(get_session)):
    if nombre:
        print("nombre: ", nombre)
        return session.exec(select(Articulo).where(Articulo.nombre==nombre).where(Articulo.esta_activo==True)).all()
    else:
        print("nombre null")
        return session.exec(select(Articulo).where(Articulo.esta_activo==True)).all()

@router.patch("/articulo/{id}")
def actualizar_articulos(id, articuloUpdate: ArticuloUpdate, session: Session = Depends(get_session)):
    articuloDb = session.exec(select(Articulo).where(Articulo.id==id).where(Articulo.esta_activo==True)).first()
    if not articuloDb:
        raise HTTPException(status_code=404, detail="Articulo not found")
    articuloData = articuloUpdate.model_dump(exclude_unset=True)
    articuloDb.sqlmodel_update(articuloData)
    session.add(articuloDb)
    session.commit()
    session.refresh(articuloDb)
    return articuloDb

@router.post("/articulos")
def crear_articulo(articulo: Articulo, session: Session = Depends(get_session)):
    articulo.esta_activo = True
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    return articulo

@router.delete("/articulos/{id}")
def crear_articulo(id, session: Session = Depends(get_session)):
    articulo = session.exec(select(Articulo).where(Articulo.id==id)).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo not found")
    articulo.esta_activo = False
    session.add(articulo)
    session.commit()
    session.refresh(articulo)
    return articulo