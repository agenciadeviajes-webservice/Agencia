# app/Dominio/paquetes_model.py (MODIFICADO)
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Any
from fastapi import status # <-- Nuevo import para códigos de error

# --- MODELOS BASE ---

# Modelo general para TODAS las respuestas de la API
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None # Puede ser un objeto, una lista o un diccionario vacío
    error_code: int = status.HTTP_200_OK # Código HTTP a usar si success=False

# --- MODELO DE CREACIÓN (HU-02: POST) ---
class PaqueteCreate(BaseModel):
    destino: str
    fecha_inicio: date
    fecha_fin: date
    # Validamos que el precio sea mayor a cero (gt=0)
    precio: float = Field(gt=0, description="El precio debe ser mayor a cero.")
    tipo_paquete: str
    tours_incluidos: str
    cupos: int = Field(ge=0, description="Los cupos no pueden ser negativos.")


# --- MODELO DE RESPUESTA DE ÉXITO (HU-02: Data) ---
class PaqueteData(BaseModel):
    id_paquete: int = Field(alias='id')
    destino: str
    precio: float
    fecha_inicio: date
    fecha_fin: date
    estado: str = "Disponible"

    class Config:
        from_attributes = True
        populate_by_name = True

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

# --- [NUEVO] MODELO PARA DATA DE ELIMINACIÓN (HU-04) ---
class PaqueteDeleteData(BaseModel):
    id_paquete: int