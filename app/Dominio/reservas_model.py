# app/Dominio/reservas_model.py
from pydantic import BaseModel, Field
from typing import Optional, Any
from fastapi import status
# Asumimos que APIResponse está disponible vía import o se copia aquí

# --- MODELO DE SOLICITUD (REQUEST BODY) ---
class ReservaCreate(BaseModel):
    idCliente: int = Field(..., gt=0)
    idPaquete: int = Field(..., gt=0)
    numeroPersonas: int = Field(..., gt=0)
    metodoPago: str

# --- MODELO DE DATA EN RESPUESTA EXITOSA ---
class ReservaData(BaseModel):
    idReserva: int
    idCliente: int
    idPaquete: int
    numeroPersonas: int
    metodoPago: str
    estado: str
    
# --- (APIResponse debería estar importado o definido) ---
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[int] = status.HTTP_200_OK
    details: Optional[str] = None