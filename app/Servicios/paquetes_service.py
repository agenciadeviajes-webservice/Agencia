# app/Servicios/paquetes_service.py (NUEVO ARCHIVO)
from sqlalchemy.orm import Session
from app.repositorio.paquetes_repository import PaquetesRepository
from app.dominio.paquetes_model import PaqueteListResponse, PaqueteListItem, PaqueteCreate, APIResponse, PaqueteData, PaqueteDeleteData
from app.database import PaqueteDB
from fastapi import status 
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
        
    def actualizar_paquete(self, paquete_id: int, paquete_data: PaqueteCreate) -> APIResponse:
        
        # 1. Verificar Existencia (HU-03: 404)
        paquete_existente = self.repository.obtener_por_id(paquete_id)
        if not paquete_existente:
            return APIResponse(
                success=False,
                message="No se encontró el paquete turístico o no fue posible actualizarlo.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        # 2. Validación de Negocio: Fechas Coherentes (HU-03: 400)
        if paquete_data.fecha_inicio >= paquete_data.fecha_fin:
            return APIResponse(
                success=False,
                message="Error en los datos enviados. La fecha de fin debe ser posterior a la de inicio.",
                error_code=status.HTTP_400_BAD_REQUEST 
            )

        # 3. Preparar datos y Actualizar
        try:
            # Convertir Pydantic a diccionario para pasar al Repositorio
            datos_a_actualizar = paquete_data.model_dump()
            
            paquete_actualizado = self.repository.actualizar_paquete(
                paquete_existente, 
                datos_a_actualizar
            )

            # 4. Éxito (HTTP 200)
            data_respuesta = PaqueteData.model_validate(paquete_actualizado)
            
            return APIResponse(
                success=True,
                message="Paquete turístico actualizado correctamente",
                data=data_respuesta
            )
            
        except Exception as e:
            # 5. Error Interno (HU-03: 500)
            print(f"Error al actualizar paquete ID {paquete_id}: {e}")
            return APIResponse(
                success=False,
                message="No fue posible actualizar el paquete turístico en este momento.",
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def eliminar_paquete(self, id_paquete: int) -> APIResponse:
        
        # 1. Verificar Existencia (HU-04: Caso 2 - 404)
        paquete_existente = self.repository.obtener_por_id(id_paquete)
        if not paquete_existente:
            return APIResponse(
                success=False,
                message="No fue posible eliminar el paquete turístico. Verifique el ID proporcionado.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        try:
            # 2. Intentar Eliminar en BD
            self.repository.eliminar_paquete(paquete_existente)

            # 3. Respuesta Exitosa (HU-04: Caso 1 - 200)
            return APIResponse(
                success=True,
                message="Paquete turístico eliminado correctamente",
                data=PaqueteDeleteData(id_paquete=id_paquete)
            )
            
        except Exception as e:
            # 4. Error en Base de Datos (HU-04: Caso 3 - 500)
            # Esto pasa si el paquete tiene reservas asociadas u otro error de SQL
            print(f"Error al eliminar paquete ID {id_paquete}: {e}")
            return APIResponse(
                success=False,
                message="Error interno al intentar eliminar el paquete turístico.",
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )