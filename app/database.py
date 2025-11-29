from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

# Configuración de Conexión
DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 1. TABLA CLIENTES/USUARIOS (HU-05 y HU-06)
class UserDB(Base):
    __tablename__ = "usuarios" 

    id = Column(Integer, primary_key=True, index=True)
    documento = Column(String, unique=True, index=True, nullable=False) # Agregado HU-05
    name = Column(String, nullable=False)
    telefono = Column(String, nullable=False) # Agregado HU-05
    email = Column(String, unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False) # Agregado HU-05
    password_hashed = Column(String, nullable=False) # Agregado HU-06 (Login)


# 2. TABLA PAQUETES (HU-04)
class PaqueteDB(Base):
    __tablename__ = "paquetes"

    id = Column(Integer, primary_key=True, index=True)
    destino = Column(String, nullable=False, index=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    precio = Column(Float, nullable=False) 
    tipo_paquete = Column(String)
    tours_incluidos = Column(String) 
    cupos = Column(Integer, default=0)

class ReservaDB(Base):
    __tablename__ = 'reserva'

    id = Column(Integer, primary_key=True, index=True)
    # Necesario para validar el monto del pago
    monto_total = Column(Float, nullable=False) 
    # Necesario para verificar el estado y actualizarlo
    estado = Column(String, default="Pendiente", nullable=False) 

# --- MODELO DE PAGO (Para registrar la transacción) ---
class PagoDB(Base):
    __tablename__ = 'pago'

    id = Column(Integer, primary_key=True, index=True)
    id_reserva = Column(Integer, ForeignKey('reserva.id'), nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String, nullable=False)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    estado_pago = Column(String, default="Exitoso", nullable=False)

    # Relación para obtener la reserva
    reserva = relationship("ReservaDB")


# CREACIÓN DE TABLAS
# ESTE COMANDO CREA AMBAS TABLAS (usuarios y paquetes) a la vez.
# Va fuera de cualquier clase.
Base.metadata.create_all(bind=engine)