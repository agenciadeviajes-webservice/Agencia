from sqlalchemy.orm import Session
from datetime import date

from app.repositorio.usuarios_repository import UsuariosRepository
from app.dominio.usuarios_model import UserCreate, APIResponse, UserData

class UsuariosService:

    def __init__(self, db: Session):
        self.repository = UsuariosRepository(db)

    def calculate_age(self, born: date):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def create_user(self, user_data: UserCreate) -> APIResponse:
        # 1. Validar documento duplicado
        if self.repository.get_user_by_documento(user_data.documento):
            return APIResponse(
                success=False,
                message="Error en la validación",
                error_code=400,
                details="El documento ya se encuentra registrado"
            )

        # 2. Validar edad (Regla de negocio)
        age = self.calculate_age(user_data.fecha_nacimiento)
        if age < 18:
            return APIResponse(
                success=False,
                message="Error en la validación",
                error_code=400,
                details="La edad mínima para registrarse es de 18 años"
            )

        # 3. Validar email duplicado
        if self.repository.get_user_by_email(user_data.email):
             return APIResponse(
                success=False,
                message="Error en la validación",
                error_code=400,
                details="El correo ya se encuentra registrado"
            )

        # 4. Crear usuario si todo está bien
        new_user = self.repository.create_user(user_data)
        
        # Convertimos a esquema Pydantic para la respuesta
        user_response_data = UserData.from_orm(new_user)

        return APIResponse(
            success=True,
            message="Cliente registrado exitosamente",
            data=user_response_data
        )