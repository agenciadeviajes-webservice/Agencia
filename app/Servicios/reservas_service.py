# app/Servicios/reservas_service.py
from sqlalchemy.orm import Session
from app.repositorio.reservas_repository import ReservasRepository
from app.dominio.reservas_model import ReservaCreate, APIResponse, ReservaData
from fastapi import status

class ReservasService:
    def __init__(self, db: Session):
        self.repository = ReservasRepository(db)

    def crear_reserva(self, data: ReservaCreate) -> APIResponse:
        
        try:
            # 1. Validación de existencia: Cliente (HU-11: Caso 3 - 404)
            cliente = self.repository.obtener_cliente(data.idCliente)
            if not cliente:
                return APIResponse(
                    success=False,
                    message="Error al crear reserva",
                    data={"details": f"Cliente con ID {data.idCliente} no encontrado."},
                    error_code=status.HTTP_404_NOT_FOUND
                )

            # 2. Validación de existencia: Paquete (HU-11: Caso 3 - 404)
            paquete = self.repository.obtener_paquete(data.idPaquete)
            if not paquete:
                return APIResponse(
                    success=False,
                    message="Error al crear reserva",
                    data={"details": f"Paquete con ID {data.idPaquete} no encontrado."},
                    error_code=status.HTTP_404_NOT_FOUND
                )
            
            # 3. Validación de cupos (HU-11: Caso 2 - 400)
            if paquete.cupos < data.numeroPersonas:
                return APIResponse(
                    success=False,
                    message="Error en la validación",
                    data={"details": "Cupos insuficientes en el paquete"},
                    error_code=status.HTTP_400_BAD_REQUEST
                )

            # 4. Crear Reserva
            reserva_db = self.repository.crear_reserva(data, paquete)

            # 5. Respuesta Exitosa (HU-11: Caso 1 - 200)
            reserva_data_response = ReservaData(
                idReserva=reserva_db.id,
                idCliente=reserva_db.id_cliente,
                idPaquete=reserva_db.id_paquete,
                numeroPersonas=reserva_db.numero_personas,
                metodoPago=reserva_db.metodo_pago,
                estado=reserva_db.estado
            )

            return APIResponse(
                success=True,
                message="Reserva creada en estado pendiente",
                data=reserva_data_response
            )

        except Exception as e:
            # 6. Error Interno (HU-11: Caso 4 - 500)
            print(f"Error interno al crear reserva: {e}")
            return APIResponse(
                success=False,
                message="Error interno del servidor",
                data={"details": "Falla de conexión a la base de datos o error inesperado."},
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def cancelar_reserva(self, id_reserva: int) -> APIResponse:
        try:
            # 1. Verificar existencia de reserva
            reserva = self.repository.obtener_reserva(id_reserva)
            if not reserva:
                return APIResponse(
                    success=False,
                    message="Reserva no encontrada o no puede ser cancelada",
                    data=None,
                    error_code=status.HTTP_404_NOT_FOUND,
                    details="ID de reserva inválido"
                )

            # 2. Validar estado permitido
            if reserva.estado not in ["Pendiente", "Confirmada"]:
                return APIResponse(
                    success=False,
                    message="No se puede cancelar esta reserva",
                    data=None,
                    error_code=status.HTTP_400_BAD_REQUEST,
                    details=f"Estado actual: {reserva.estado}"
                )

            # 3. Obtener paquete
            paquete = self.repository.obtener_paquete(reserva.id_paquete)
            if not paquete:
                return APIResponse(
                    success=False,
                    message="Error interno",
                    data=None,
                    error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    details="Paquete asociado no existe"
                )

            # 4. Cancelar reserva
            reserva_cancelada = self.repository.cancelar_reserva(reserva, paquete)

            data_response = {
                "idReserva": reserva_cancelada.id,
                "estado": reserva_cancelada.estado
            }

            return APIResponse(
                success=True,
                message="Reserva cancelada exitosamente",
                data=data_response
            )

        except Exception as e:
            print(f"[ERROR] cancelar_reserva: {e}")
            return APIResponse(
                success=False,
                message="Error interno del servidor",
                data=None,
                error_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                details=str(e)
            )
