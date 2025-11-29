# app/Api/pagos_api.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

# Asume que tienes un SessionLocal para get_db, como en el módulo de paquetes
from app.database import SessionLocal # Asumiendo este import
from app.servicios.pagos_service import PagosService
from app.dominio.pagos_model import PagoCreate, APIResponse # Importa los modelos

router = APIRouter(prefix="/api/v1/pagos", tags=["Pagos"])

# Función de dependencia de DB (asumimos que la tienes definida en un archivo)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTA HU-13: REGISTRAR PAGO ---
@router.post("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
def registrar_pago(
    pago_data: PagoCreate, # FastAPI infiere que es el JSON Body
    response: Response = Response(),
    db: Session = Depends(get_db)
):
    """
    [HU-13] Registra un pago y actualiza el estado de una reserva.
    """
    service = PagosService(db)
    result = service.registrar_pago(pago_data)

    if not result.success:
        # Controlamos el código HTTP según el error que vino del servicio (400, 404, 500)
        response.status_code = result.error_code
    
    return result

@router.put("/{idReserva}/confirmar", response_model=APIResponse, status_code=status.HTTP_200_OK)
def confirmar_pago(
    idReserva: int,
    response: Response = Response(),
    db: Session = Depends(get_db)
):
    """
    [HU-21] Confirma un pago registrado (estado 'Exitoso') y actualiza la reserva a 'Confirmada'.
    """
    service = PagosService(db)
    result = service.confirmar_pago(idReserva)

    if not result.success:
        # Controlamos el código HTTP según el error (404, 500)
        response.status_code = result.error_code
    
    return result