from fastapi import APIRouter

router = APIRouter(
    prefix="/incidentes",
    tags=["incidentes"],
)


@router.get("/tickets")
def obtener_tickets():
    return [{"id": 1, "descripcion": "se rompio"}, {"id": 2, "descripcion": "bug"}]
