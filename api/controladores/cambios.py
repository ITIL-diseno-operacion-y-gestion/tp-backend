from fastapi import APIRouter

router = APIRouter(
    prefix="/cambios",
    tags=["cambios"],
)


@router.get("")
def algo():
    return "gestion de cambios"
