from sqlalchemy.orm import Session
from app.database import UserDB
from app.dominio.usuarios_model import UserCreate

class UsuariosRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserDB:
        db_user = UserDB(
            documento=user.documento,
            name=user.name,
            telefono=user.telefono,
            email=user.email,
            fecha_nacimiento=user.fecha_nacimiento
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_documento(self, documento: str) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.documento == documento).first()

    def get_user_by_email(self, email: str) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.email == email).first()