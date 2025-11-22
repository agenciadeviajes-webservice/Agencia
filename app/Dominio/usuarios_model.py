from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    # Lo que envia el frontend
    documento: str
    name: str
    telefono: str
    email: EmailStr
    fecha_nacimiento: date # Pydantic valida formato YYYY-MM-DD

class UserData(BaseModel):
    # Datos internos del usuario para la respuesta
    id: int
    documento: str
    name: str
    telefono: str
    email: str
    fecha_nacimiento: date

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    # La respuesta "envoltorio" estandarizada
    success: bool
    message: str
    data: Optional[UserData] = None
    error_code: Optional[int] = None
    details: Optional[str] = None