from pydantic import BaseModel, EmailStr
# Pydantic valida automáticamente tipos de datos
# EmailStr valida que sea un formato de email correcto
class UserCreate(BaseModel):
# Modelo para CREAR un usuario (datos que envía el cliente)
name: str
# name debe ser texto (string)
email: EmailStr
# email debe tener formato válido (ej: usuario@ejemplo.com)
age: int
# age debe ser un número entero
class UserResponse(BaseModel):
# Modelo para MOSTRAR un usuario (datos que devuelve la API)
id: int
# Incluye el ID asignado por la base de datos
name: str
email: str
age: int
class Config:
# Configuración especial de Pydantic
from_attributes = True
# Permite convertir objetos de SQLAlchemy a Pydantic