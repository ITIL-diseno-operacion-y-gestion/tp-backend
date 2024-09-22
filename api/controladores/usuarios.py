from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get("")
def obtener_usuarios():
    return [{"nombre": "Rick"}, {"nombre": "Morty"}]