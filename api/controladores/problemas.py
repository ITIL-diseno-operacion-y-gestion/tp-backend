from fastapi import APIRouter

router = APIRouter(
    prefix="/problemas",
    tags=["problemas"],
)


@router.get("")
def algo():
    return "gestion de problemas"