from sqlalchemy.orm import Session
# Session permite hacer consultas a la base de datos
from database import UserDB
# Importa el modelo de la tabla users
class UserRepository:
# Clase que agrupa todas las operaciones de base de datos
def __init__(self, db: Session):
# Constructor: recibe una sesión de base de datos
self.db = db
# Guarda la sesión para usarla en los métodos
def create_user(self, name: str, email: str, age: int) -> UserDB:
# Método para CREAR un nuevo usuario en la base de datos
user = UserDB(name=name, email=email, age=age)
# Crea un objeto UserDB con los datos recibidos
self.db.add(user)
# Agrega el usuario a la sesión (aún no se guarda en BD)
self.db.commit()
# Confirma la transacción: ejecuta INSERT en SQLite
self.db.refresh(user)
# Actualiza el objeto con los datos de la BD (obtiene el ID asignado)
return user
# Devuelve el usuario creado con su ID
def get_user_by_id(self, user_id: int) -> UserDB:
# Método para BUSCAR un usuario por su ID
return self.db.query(UserDB).filter(UserDB.id == user_id).first()
# Ejecuta: SELECT * FROM users WHERE id = user_id LIMIT 1
def get_user_by_email(self, email: str) -> UserDB:
# Método para BUSCAR un usuario por email
return self.db.query(UserDB).filter(UserDB.email == email).first()
# Ejecuta: SELECT * FROM users WHERE email = 'email' LIMIT 1
def get_all_users(self) -> list[UserDB]:
# Método para OBTENER todos los usuarios
return self.db.query(UserDB).all()
# Ejecuta: SELECT * FROM users