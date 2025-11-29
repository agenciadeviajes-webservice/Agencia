# app/Repositorio/reservas_repository.py
from sqlalchemy.orm import Session
from app.database import ReservaDB, PaqueteDB, UserDB # Necesitamos las 3 tablas
from app.dominio.reservas_model import ReservaCreate
from typing import Optional

class ReservasRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_cliente(self, id_cliente: int) -> Optional[UserDB]:
        """Busca el cliente por ID."""
        return self.db.query(UserDB).filter(UserDB.id == id_cliente).first()

    def obtener_paquete(self, id_paquete: int) -> Optional[PaqueteDB]:
        """Busca el paquete por ID."""
        return self.db.query(PaqueteDB).filter(PaqueteDB.id == id_paquete).first()

    def crear_reserva(self, reserva_data: ReservaCreate, paquete: PaqueteDB) -> ReservaDB:
        """Crea la reserva y calcula el monto total."""
        
        # Calcular el monto total
        monto_total = paquete.precio * reserva_data.numeroPersonas
        
        nueva_reserva = ReservaDB(
            id_cliente=reserva_data.idCliente,
            id_paquete=reserva_data.idPaquete,
            numero_personas=reserva_data.numeroPersonas,
            metodo_pago=reserva_data.metodoPago,
            monto_total=monto_total,
            estado="Pendiente"
        )
        self.db.add(nueva_reserva)
        self.db.commit()
        self.db.refresh(nueva_reserva)
        
        return nueva_reserva
    
    def obtener_reserva(self, id_reserva: int) -> Optional[ReservaDB]:
        """Obtiene una reserva por ID."""
        return self.db.query(ReservaDB).filter(ReservaDB.id == id_reserva).first()

    def cancelar_reserva(self, reserva: ReservaDB, paquete: PaqueteDB) -> ReservaDB:
        """Cancela la reserva y libera cupos del paquete."""
        
        # Cambiar estado
        reserva.estado = "Cancelada"

        # Liberar cupos
        paquete.cupos += reserva.numero_personas

        # Guardar cambios
        self.db.commit()
        self.db.refresh(reserva)

        print(f"[LOG] Reserva {reserva.id} cancelada. Cupos liberados: {reserva.numero_personas}")

        return reserva
