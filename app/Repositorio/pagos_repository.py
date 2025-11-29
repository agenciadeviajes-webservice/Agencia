# app/Repositorio/pagos_repository.py
from sqlalchemy.orm import Session
from app.database import ReservaDB, PagoDB
from app.dominio.pagos_model import PagoCreate
from datetime import datetime
from typing import Optional

class PagosRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_reserva_por_id(self, id_reserva: int) -> Optional[ReservaDB]:
        """Busca la reserva para validación."""
        return self.db.query(ReservaDB).filter(ReservaDB.id == id_reserva).first()

    def registrar_pago_y_actualizar_reserva(self, id_reserva: int, data: PagoCreate, reserva: ReservaDB) -> PagoDB:
        
        # 1. Registrar Pago
        nuevo_pago = PagoDB(
            id_reserva=id_reserva,
            monto=data.monto,
            metodo_pago=data.metodoPago,
            estado_pago="Exitoso"
        )
        self.db.add(nuevo_pago)
        self.db.flush() # Guarda el pago para obtener el ID, pero no hace commit

        # 2. Actualizar estado de la Reserva
        reserva.estado = "Confirmada"
        
        self.db.commit()
        self.db.refresh(nuevo_pago)
        
        return nuevo_pago