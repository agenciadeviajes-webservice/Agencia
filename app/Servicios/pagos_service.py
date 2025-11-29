# app/Servicios/pagos_service.py
from sqlalchemy.orm import Session
from app.repositorio.pagos_repository import PagosRepository
from app.dominio.pagos_model import PagoCreate, APIResponse, PagoData
from fastapi import status

class PagosService:
    def __init__(self, db: Session):
        self.repository = PagosRepository(db)

    def registrar_pago(self, data: PagoCreate) -> APIResponse:
        
        # 1. Obtener y Validar Existencia/Estado de la Reserva (Caso 2: 404)
        reserva = self.repository.obtener_reserva_por_id(data.idReserva)
        
        if not reserva or reserva.estado != "Pendiente":
            return APIResponse(
                success=False,
                message="Error al registrar el pago",
                data={"details": "Reserva no encontrada o estado no válido (Debe ser Pendiente)"},
                error_code=status.HTTP_404_NOT_FOUND # 404
            )

        # 2. Validar Monto (Caso 3: 400)
        # Importante: Usar un margen de error pequeño para floats (ej. 0.01)
        if abs(reserva.monto_total - data.monto) > 0.01:
            return APIResponse(
                success=False,
                message="Error en la validación",
                data={"details": f"El monto del pago ({data.monto}) no coincide con el total de la reserva ({reserva.monto_total})"},
                error_code=status.HTTP_400_BAD_REQUEST # 400
            )
            
        try:
            # 3. Registrar Pago y Actualizar Reserva
            pago_db = self.repository.registrar_pago_y_actualizar_reserva(data.idReserva, data, reserva)

            # 4. Respuesta Exitosa (Caso 1: 200)
            pago_data_response = PagoData(
                idPago=pago_db.id,
                idReserva=pago_db.id_reserva,
                monto=pago_db.monto,
                metodoPago=pago_db.metodo_pago,
                estadoPago=pago_db.estado_pago,
                estadoReserva=reserva.estado # Ya está en "Confirmada"
            )

            return APIResponse(
                success=True,
                message="Pago registrado exitosamente y reserva confirmada",
                data=pago_data_response
            )

        except Exception as e:
            # 5. Error Interno (Caso 4: 500)
            print(f"Error interno durante el registro de pago y actualización de reserva: {e}")
            return APIResponse(
                success=False,
                message="Error interno del servidor. Intente más tarde.",
                data={"details": "Falla de conexión a la base de datos o error de integridad."},
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR # 500
            )