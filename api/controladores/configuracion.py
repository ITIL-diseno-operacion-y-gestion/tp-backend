from fastapi import APIRouter

router = APIRouter(
    prefix="/configuracion",
    tags=["configuracion"],
)


@router.get("/articulos")
def obtener_articulos():
    return [{"id": 1, "tipo": "hardware"}, {"id": 2, "tipo": "software"}]
