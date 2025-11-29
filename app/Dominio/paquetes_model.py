# app/Dominio/paquetes_model.py (MODIFICADO)
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# --- (PaqueteCreate se mantiene) ---

# Modelo para un paquete individual en la respuesta de la lista
class PaqueteListItem(BaseModel):
    id_paquete: int = Field(alias='id')
    nombre: str = Field(alias='destino') # Usaremos el campo 'destino' como 'nombre'
    destino: str
    precio: float
    fecha_inicio: date
    fecha_fin: date
    estado: str = "Disponible" # Asumimos que si aparece, está disponible

    class Config:
        from_attributes = True
        populate_by_name = True

# Modelo de Respuesta Estandarizada para Listas
class PaqueteListResponse(BaseModel):
    success: bool
    mensaje: str = Field(alias='message')
    data: List[PaqueteListItem]