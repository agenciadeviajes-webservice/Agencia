# app/Servicios/paquetes_service.py (NUEVO ARCHIVO)
from sqlalchemy.orm import Session
from app.repositorio.paquetes_repository import PaquetesRepository
from app.dominio.paquetes_model import PaqueteListResponse, PaqueteListItem, PaqueteCreate, APIResponse, PaqueteData
from app.database import PaqueteDB
from fastapi import status # <-- Nuevo import
from typing import List

class PaquetesService:

    def __init__(self, db: Session):
        self.repository = PaquetesRepository(db)

    def listar_paquetes(self) -> PaqueteListResponse:
        
        # 1. Obtener datos del Repositorio
        paquetes_db = self.repository.listar_todos_los_paquetes()
        
        # 2. Caso: SIN DATOS (HU-04, Criterio 2)
        if not paquetes_db:
            return PaqueteListResponse(
                success=False,
                message="No existen paquetes turísticos registrados en este momento",
                data=[]
            )

        # 3. Caso: ÉXITO (HU-04, Criterio 2)
        
        # Convertir los objetos PaqueteDB a la lista de esquemas Pydantic
        paquetes_lista = [PaqueteListItem.from_orm(p) for p in paquetes_db]

        return PaqueteListResponse(
            success=True,
            message="Consulta de paquetes exitosa",
            data=paquetes_lista
        )
    
    def crear_paquete(self, paquete: PaqueteCreate) -> APIResponse:
        
        # 1. Validación de Negocio: Fechas Coherentes (fecha_fin > fecha_inicio)
        if paquete.fecha_inicio >= paquete.fecha_fin:
            return APIResponse(
                success=False,
                message="Error de validación: La fecha de fin debe ser posterior a la fecha de inicio.",
                error_code=status.HTTP_400_BAD_REQUEST # Error de validación de datos
            )
            
        # 2. Mapear Pydantic a Modelo de Base de Datos
        paquete_db = PaqueteDB(
            destino=paquete.destino,
            fecha_inicio=paquete.fecha_inicio,
            fecha_fin=paquete.fecha_fin,
            precio=paquete.precio,
            tipo_paquete=paquete.tipo_paquete,
            tours_incluidos=paquete.tours_incluidos,
            cupos=paquete.cupos
        )
        
        try:
            # 3. Guardar en Repositorio
            nuevo_paquete = self.repository.crear_paquete(paquete_db)

            # 4. Éxito
            data_respuesta = PaqueteData.model_validate(nuevo_paquete)

            return APIResponse(
                success=True,
                message="Paquete turístico registrado correctamente",
                data=data_respuesta
            )
            
        except Exception as e:
            # 5. Error Interno (Base de datos o servidor)
            print(f"Error al crear paquete: {e}")
            return APIResponse(
                success=False,
                message="No fue posible registrar el paquete turístico en este momento.",
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )