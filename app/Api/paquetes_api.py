# app/Api/paquetes_api.py (NUEVO ARCHIVO)
from fastapi import APIRouter, Depends, status, Response, Path
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.servicios.paquetes_service import PaquetesService
from app.dominio.paquetes_model import PaqueteListResponse, PaqueteCreate, APIResponse

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

@router.post("/", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
# Usamos HTTP 201 para éxito
def crear_paquete(paquete: PaqueteCreate, response: Response, db: Session = Depends(get_db)):
    """
    [HU-02] Registra un nuevo paquete turístico con validaciones.
    """
    service = PaquetesService(db)
    result = service.crear_paquete(paquete)

    if not result.success:
        # Si la operación falla (400 por validación de fechas o 500 por error interno)
        # Seteamos el código HTTP de la respuesta con el error_code que nos da el servicio.
        response.status_code = result.error_code
    
    return result

@router.put("/{id_paquete}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def actualizar_paquete(
    # 1. MOVER PAQUETE AL PRINCIPIO: Ahora es el primer argumento (obligatorio)
    paquete: PaqueteCreate, 
    
    # 2. El resto de argumentos con valor por defecto van después
    id_paquete: int = Path(..., gt=0), 
    response: Response = Response(),
    db: Session = Depends(get_db)
):
    """
    [HU-03] Actualiza un paquete turístico existente por su ID.
    """
    service = PaquetesService(db)
    result = service.actualizar_paquete(id_paquete, paquete)

    if not result.success:
        # Seteamos el código HTTP según el error (404, 400, o 500)
        response.status_code = result.error_code
    
    return result