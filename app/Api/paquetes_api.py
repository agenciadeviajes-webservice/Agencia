# app/Api/paquetes_api.py (NUEVO ARCHIVO)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.servicios.paquetes_service import PaquetesService
from app.dominio.paquetes_model import PaqueteListResponse

router = APIRouter(prefix="/api/v1/paquetes", tags=["Paquetes"])

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=PaqueteListResponse, status_code=status.HTTP_200_OK)
def listar_paquetes(db: Session = Depends(get_db)):
    """
    [HU-04] Lista todos los paquetes turísticos disponibles.
    Devuelve HTTP 200 siempre, usando 'success: false' para indicar ausencia de datos.
    """
    service = PaquetesService(db)
    return service.listar_paquetes()