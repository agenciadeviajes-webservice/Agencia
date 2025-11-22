from fastapi import APIRouter

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

@router.get("/")
def listar_reservas():
    return {"mensaje": "Listado de reservas"}
