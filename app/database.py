from sqlalchemy import create_engine, Column, Integer, String
# Importa herramientas de SQLAlchemy para crear la base de datos
from sqlalchemy.ext.declarative import declarative_base
# Para crear una clase base que usarán todos los modelos
from sqlalchemy.orm import sessionmaker
# Para crear sesiones que permiten hacer consultas a la BD

DATABASE_URL = "sqlite:///./usuarios.db"
# La ruta donde se guardará el archivo de base de datos SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Crea el motor de base de datos que conectará con SQLite
# check_same_thread=False permite usar SQLite con FastAPI

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Crea una fábrica de sesiones para interactuar con la BD
# autocommit=False: los cambios deben confirmarse manualmente con commit()

Base = declarative_base()
# Clase base para todos los modelos de la base de datos


class UserDB(Base):
    # Define la estructura de la tabla "usuarios" en la base de datos
    __tablename__ = "usuarios"  
    # Nombre de la tabla en SQLite

    id = Column(Integer, primary_key=True, index=True)
    # Columna 'id': número entero, clave primaria, se autoincrementa

    name = Column(String, nullable=False)
    # Columna 'name': texto, obligatorio (no puede estar vacío)

    email = Column(String, unique=True, nullable=False)
    # Columna 'email': texto único (no se pueden repetir emails), obligatorio

    age = Column(Integer)
    # Columna 'age': número entero, opcional


Base.metadata.create_all(bind=engine)
# Crea todas las tablas en la base de datos (ejecuta CREATE TABLE)
