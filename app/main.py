from fastapi import FastAPI
# Importa la clase principal de FastAPI
from config.routers import ROUTERS
# Importa la lista de TODOS los routers configurados
app = FastAPI(
# Crea la aplicación FastAPI
title="User API",
# Título que aparece en Swagger UI
description="API con arquitectura en capas",
# Descripción en la documentación
version="1.0.0"
# Versión de la API
)
# Registra TODOS los routers automáticamente desde config/routers.py
for router in ROUTERS:
# Recorre cada router en la lista ROUTERS
app.include_router(router)
# Registra el router en la aplicación
# Automáticamente registra user_api, product_api, order_api, etc.
@app.get("/")
# Endpoint raíz (opcional, para verificar que la API funciona)
def root():
return {"message": "API funcionando correctamente"}
# Devuelve un mensaje JSON simple
# Para ejecutar: uvicorn main:app --reload
# --reload: reinicia automáticamente al cambiar código