from fastapi import APIRouter, Depends, status
# APIRouter agrupa endpoints, Depends inyecta dependencias
from sqlalchemy.orm import Session
from database import SessionLocal
# Fábrica de sesiones de base de datos
from services.user_service import UserService
from domain.user_model import UserCreate, UserResponse
router = APIRouter(prefix="/users", tags=["Users"])
# Crea un router con prefijo /users (todos los endpoints empiezan con /users)
# tags=["Users"] agrupa los endpoints en Swagger UI
def get_db():
# Función que proporciona una sesión de base de datos
db = SessionLocal()
# Crea una nueva sesión
try:
yield db
# Devuelve la sesión (yield permite cerrarla después)
finally:
db.close()
# Cierra la sesión al terminar (libera recursos)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# Decorador que define un endpoint POST en /users/
# response_model: formato de respuesta
# status_code=201: código de éxito para "creado"
def create_user(user: UserCreate, db: Session = Depends(get_db)):
# Función que se ejecuta cuando llega una petición POST
# user: datos del body (validados por Pydantic)
# db: sesión de BD inyectada automáticamente por Depends
"""Crea un nuevo usuario"""
# Documentación que aparece en Swagger
service = UserService(db)
# Crea una instancia del servicio con la sesión de BD
return service.create_user(user)
# Llama al servicio y devuelve el resultado
@router.get("/{user_id}", response_model=UserResponse)
# Endpoint GET para obtener un usuario por ID
# {user_id} es un parámetro de ruta (path parameter)
def get_user(user_id: int, db: Session = Depends(get_db)):
# user_id se extrae de la URL (ej: /users/1)
"""Obtiene un usuario por ID"""
service = UserService(db)
return service.get_user(user_id)
# Llama al servicio para buscar el usuario