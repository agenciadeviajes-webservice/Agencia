from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    # Modelo para CREAR un usuario (lo que envía el cliente)
    name: str
    email: EmailStr
    age: int


class UserResponse(BaseModel):
    # Modelo para MOSTRAR un usuario (lo que devuelve tu API)
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True
        # Permite convertir objetos SQLAlchemy -> Pydantic
