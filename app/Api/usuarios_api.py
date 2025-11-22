from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.servicios.usuarios_service import UsuariosService
from app.dominio.usuarios_model import UserCreate, APIResponse

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"]) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=APIResponse, status_code=status.HTTP_200_OK)
def create_client(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    """
    Registra un nuevo cliente.
    Siempre devuelve HTTP 200 si hubo conexión.
    El éxito o error se lee en el campo 'success' del JSON.
    """
    service = UsuariosService(db)
    result = service.create_user(user)
    
    # OJO: Ya NO cambiamos el response.status_code a 400.
    # Siempre dejamos que FastAPI retorne el 200 OK que definimos en el decorador.
    # El frontend leerá el JSON: { "success": false, ... } para saber que falló.
    
    return result