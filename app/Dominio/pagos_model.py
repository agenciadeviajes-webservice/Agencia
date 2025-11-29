# app/Dominio/pagos_model.py
from pydantic import BaseModel
from typing import Optional, Any
from fastapi import status

# --- MODELO DE SOLICITUD (REQUEST BODY) ---
class PagoCreate(BaseModel):
    idReserva: int
    monto: float
    metodoPago: str

# --- MODELO DE DATA EN RESPUESTA EXITOSA ---
class PagoData(BaseModel):
    idPago: int
    idReserva: int
    monto: float
    metodoPago: str
    estadoPago: str
    estadoReserva: str

# --- MODELO ESTÁNDAR DE RESPUESTA (Lo que tu API ya usa) ---
# Si ya tienes este en otro archivo (ej. paquetes_model.py), 
# puedes omitir esta parte y solo importarla.
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[int] = status.HTTP_200_OK