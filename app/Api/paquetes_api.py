from fastapi import APIRouter

router = APIRouter(
    prefix="/paquetes",
    tags=["Paquetes"]
)

@router.get("/")
def listar_paquetes():
    return {"mensaje": "Listado de paquetes"}
