from sqlalchemy.orm import Session
from app.database import UserDB


class UsuariosRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, age: int) -> UserDB:
        user = UserDB(name=name, email=email, age=age)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.id == user_id).first()

    def get_user_by_email(self, email: str) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.email == email).first()

    def get_all_users(self) -> list[UserDB]:
        return self.db.query(UserDB).all()
