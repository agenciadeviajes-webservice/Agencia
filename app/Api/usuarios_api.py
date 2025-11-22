from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.servicios.usuarios_service import UsuariosService
from app.dominio.usuarios_model import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario"""
    service = UsuariosService(db)
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por ID"""
    service = UsuariosService(db)
    return service.get_user(user_id)
