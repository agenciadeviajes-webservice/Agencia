# app/Servicios/pagos_service.py
from sqlalchemy.orm import Session
from app.repositorio.pagos_repository import PagosRepository
from app.dominio.pagos_model import PagoCreate, APIResponse, PagoData, PagoConfirmData, PagoReversarRequest, PagoReversionData
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
        
    def confirmar_pago(self, id_reserva: int) -> APIResponse:
        try:
            # 1. Obtener Reserva y Pago asociado (HU-21: Caso 2 - 404)
            reserva, pago = self.repository.obtener_reserva_y_pago(id_reserva)
            
            if not reserva:
                return APIResponse(
                    success=False,
                    message="Reserva no encontrada",
                    data={"details": f"Reserva con ID {id_reserva} no existe."},
                    error_code=status.HTTP_404_NOT_FOUND
                )
            
            # Un pago debe existir para ser confirmado, y debe estar en 'Exitoso'
            if not pago or pago.estado_pago != "Exitoso":
                return APIResponse(
                    success=False,
                    message="Reserva no encontrada o pago ya confirmado",
                    data={"details": "No hay un pago 'Exitoso' pendiente de confirmación para esta reserva."},
                    error_code=status.HTTP_404_NOT_FOUND
                )
            
            # 2. Confirmar Pago y Reserva (HU-21: Caso 1 - 200)
            reserva_actualizada, pago_actualizado = self.repository.confirmar_pago_y_reserva(reserva, pago)
            
            # 3. Respuesta Exitosa
            confirm_data = PagoConfirmData(
                idReserva=id_reserva,
                estadoPago=pago_actualizado.estado_pago,
                estadoReserva=reserva_actualizada.estado
            )
            
            return APIResponse(
                success=True,
                message="Pago confirmado y reserva actualizada",
                data=confirm_data
            )
        
        except Exception as e:
            # 4. Error Interno (HU-21: Caso 3 - 500)
            print(f"Error interno al confirmar pago: {e}")
            # Aquí podrías registrar el log de la excepción
            return APIResponse(
                success=False,
                message="Error interno del servidor",
                data={"details": "Falla de conexión a la base de datos o error inesperado."},
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def reversar_pago(self, id_pago: int, data: PagoReversarRequest) -> APIResponse:
        try:
            # 1. Obtener Pago (HU-22: Caso 2 - 404)
            pago = self.repository.obtener_pago_con_reserva(id_pago)
            
            if not pago:
                return APIResponse(
                    success=False,
                    message="Pago no encontrado o ya revertido",
                    data={"details": f"Pago con ID {id_pago} no existe."},
                    error_code=status.HTTP_404_NOT_FOUND
                )
            
            # 2. Validación de estado previo: Debe estar 'Confirmado'
            if pago.estado_pago != "Confirmado":
                return APIResponse(
                    success=False,
                    message="Pago no encontrado o ya revertido",
                    data={"details": f"El pago (ID {id_pago}) no está 'Confirmado' (Estado actual: {pago.estado_pago})."},
                    error_code=status.HTTP_404_NOT_FOUND
                )
            
            # 3. Reversar Pago y Reserva (HU-22: Caso 1 - 200)
            reserva_actualizada, pago_actualizado = self.repository.reversar_pago_y_reserva(pago, data.motivo)
            
            # 4. Respuesta Exitosa
            reversion_data = PagoReversionData(
                idPago=id_pago,
                idReserva=reserva_actualizada.id,
                estadoPago=pago_actualizado.estado_pago,
                estadoReserva=reserva_actualizada.estado
            )
            
            return APIResponse(
                success=True,
                message="Pago revertido exitosamente",
                data=reversion_data
            )
        
        except Exception as e:
            # 5. Error Interno (HU-22: Caso 3 - 500)
            print(f"Error interno al reversar pago: {e}")
            return APIResponse(
                success=False,
                message="Error interno al procesar la reversión",
                data={"details": "Falla de conexión a la base de datos o error inesperado."},
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )