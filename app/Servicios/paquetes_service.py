# app/Servicios/paquetes_service.py (NUEVO ARCHIVO)
from sqlalchemy.orm import Session
from app.repositorio.paquetes_repository import PaquetesRepository
from app.dominio.paquetes_model import PaqueteListResponse, PaqueteListItem
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