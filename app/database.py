from sqlalchemy import create_engine, Column, Integer, String, Date # <--- Agregamos Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "usuarios" 

    id = Column(Integer, primary_key=True, index=True)
    # Nuevos campos segun HU-05
    documento = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False) # Usamos tipo Date

Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)
# Crea todas las tablas en la base de datos (ejecuta CREATE TABLE)
