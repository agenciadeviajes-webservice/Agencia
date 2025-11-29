# app/Repositorio/paquetes_repository.py (NUEVO ARCHIVO)
from sqlalchemy.orm import Session
from app.database import PaqueteDB

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