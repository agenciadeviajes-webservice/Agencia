from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Crear la instancia de FastAPI
app = FastAPI(
    title="Mi API con FastAPI",
    description="API RESTful profesional",
    version="1.0.0"
)

# Ruta raíz
@app.get("/")
async def root():
    """
    Endpoint de bienvenida.
    """
    return {
        "message": "¡Bienvenido a mi API con FastAPI!",
        "status": "online",
        "version": "1.0.0"
    }

# Endpoint con parámetros
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """
    Ejemplo con parámetros de ruta y query.
    """
    return {
        "item_id": item_id,
        "query": q
    }

# Health check
@app.get("/health")
async def health_check():
    """
    Verifica el estado del servidor.
    """
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )