# app/Api/reservas_api.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

# Asume que tienes SessionLocal y get_db definidos o importados
from app.database import SessionLocal # Asumiendo este import
from app.servicios.reservas_service import ReservasService
from app.dominio.reservas_model import ReservaCreate, APIResponse

router = APIRouter(prefix="/api/v1/reservas", tags=["Reservas"])

# Función de dependencia de DB (asumimos que la tienes definida en un archivo)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTA HU-11: CREAR RESERVA ---
@router.post("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
def crear_reserva(
    reserva_data: ReservaCreate, 
    response: Response = Response(),
    db: Session = Depends(get_db)
):
    """
    [HU-11] Crea una nueva reserva para un paquete turístico.
    """
    service = ReservasService(db)
    result = service.crear_reserva(reserva_data)

    if not result.success:
        # Controlamos el código HTTP según el error (400, 404, 500)
        response.status_code = result.error_code
    
    return result

@router.delete("/{idReserva}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def cancelar_reserva(
    idReserva: int,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    [HU-25] Cancelar Reserva
    """
    service = ReservasService(db)
    result = service.cancelar_reserva(idReserva)

    if not result.success:
        response.status_code = result.error_code
    
    return result
