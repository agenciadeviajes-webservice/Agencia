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
    
    def obtener_reserva_y_pago(self, id_reserva: int) -> tuple[Optional[ReservaDB], Optional[PagoDB]]:
        """Busca la reserva y el último pago registrado para esa reserva."""
        reserva = self.db.query(ReservaDB).filter(ReservaDB.id == id_reserva).first()
        
        # Buscar el último pago registrado (el que tiene estado "Exitoso")
        pago = (
            self.db.query(PagoDB)
            .filter(PagoDB.id_reserva == id_reserva)
            .order_by(PagoDB.fecha_pago.desc()) # Último pago primero
            .first()
        )
        return reserva, pago

    def confirmar_pago_y_reserva(self, reserva: ReservaDB, pago: PagoDB):
        """Actualiza el estado del pago y de la reserva."""
        
        # Actualizar Pago
        pago.estado_pago = "Confirmado"
        
        # Actualizar Reserva
        reserva.estado = "Confirmada" 
        
        self.db.commit()
        self.db.refresh(reserva)
        self.db.refresh(pago)
        
        return reserva, pago
    
    def obtener_pago_con_reserva(self, id_pago: int) -> Optional[PagoDB]:
        """Busca el pago por ID, cargando la relación a la Reserva."""
        return self.db.query(PagoDB).filter(PagoDB.id == id_pago).first()

    def reversar_pago_y_reserva(self, pago: PagoDB, motivo: str):
        """Actualiza el estado del pago a 'Revertido' y la reserva a 'Cancelada'."""
        
        # El pago debe existir y tener la relación de reserva
        reserva: ReservaDB = pago.reserva 
        
        # 1. Actualizar Pago
        pago.estado_pago = "Revertido"
        # Opcional: Podrías añadir un campo en PagoDB para guardar el motivo
        
        # 2. Actualizar Reserva
        reserva.estado = "Cancelada" # La reversión implica una cancelación efectiva
        
        self.db.commit()
        self.db.refresh(reserva)
        self.db.refresh(pago)
        
        return reserva, pago