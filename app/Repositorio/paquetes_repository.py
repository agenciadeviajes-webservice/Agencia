# app/Repositorio/paquetes_repository.py (NUEVO ARCHIVO)
from sqlalchemy.orm import Session
from app.database import PaqueteDB
from typing import Optional

class PaquetesRepository:

    def __init__(self, db: Session):
        self.db = db

    # Método de la HU-04
    def listar_todos_los_paquetes(self) -> list[PaqueteDB]:
        # Aquí puedes agregar un filtro si la tabla PaqueteDB tuviera un campo 'estado'
        # Por ahora, listamos todos:
        return self.db.query(PaqueteDB).all()

    # --- (Aquí irán los métodos para crear, actualizar y eliminar) ---
    def crear_paquete(self, paquete_data: PaqueteDB) -> PaqueteDB:
        """Guarda un nuevo paquete en la base de datos y lo retorna."""
        self.db.add(paquete_data)
        self.db.commit()
        self.db.refresh(paquete_data)
        return paquete_data
    
    # --- MÉTODO HU-03: BUSCAR POR ID ---
    def obtener_por_id(self, paquete_id: int) -> Optional[PaqueteDB]:
        """Busca un paquete por su ID."""
        return self.db.query(PaqueteDB).filter(PaqueteDB.id == paquete_id).first()

    # --- MÉTODO HU-03: ACTUALIZAR ---
    def actualizar_paquete(self, paquete_existente: PaqueteDB, datos_actualizados: dict) -> PaqueteDB:
        """Aplica los cambios del diccionario al objeto DB y lo guarda."""
        for key, value in datos_actualizados.items():
            # Asume que los datos_actualizados son los campos del modelo PaqueteDB
            setattr(paquete_existente, key, value)
        
        self.db.commit()
        self.db.refresh(paquete_existente)
        return paquete_existente