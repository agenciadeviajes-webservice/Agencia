from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
# Importa el repositorio para interactuar con la BD
from domain.user_model import UserCreate, UserResponse
# Importa los modelos Pydantic
from fastapi import HTTPException
# Para lanzar errores HTTP con códigos de estado
class UserService:
# Clase que contiene la lógica de negocio
def __init__(self, db: Session):
self.repository = UserRepository(db)
# Crea una instancia del repositorio
def create_user(self, user_data: UserCreate) -> UserResponse:
# Método para crear un usuario (con validaciones de negocio)
existing_user = self.repository.get_user_by_email(user_data.email)
# Busca si ya existe un usuario con ese email
if existing_user:
# Si existe, lanza un error
raise HTTPException(status_code=400, detail="Email ya registrado")
# Error 400 Bad Request con mensaje descriptivo
if user_data.age < 18:
# Validación de negocio: debe ser mayor de edad
raise HTTPException(status_code=400, detail="Debe ser mayor de edad")
user = self.repository.create_user(
# Si pasa todas las validaciones, llama al repositorio
name=user_data.name,
email=user_data.email,
age=user_data.age
)
return UserResponse.from_orm(user)
# Convierte el objeto UserDB a UserResponse (Pydantic)
def get_user(self, user_id: int) -> UserResponse:
# Método para obtener un usuario por ID
user = self.repository.get_user_by_id(user_id)
# Busca el usuario en la base de datos
if not user:
# Si no existe, lanza error 404
raise HTTPException(status_code=404, detail="Usuario no encontrado")
return UserResponse.from_orm(user)