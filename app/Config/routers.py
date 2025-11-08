from api import user_api
# Importa el router de usuarios
from api import product_api
# Importa el router de productos
from api import order_api
# Importa el router de órdenes
# Lista de todos los routers que se registrarán en la aplicación
ROUTERS = [
# Cada elemento es un router que tiene endpoints
usuario_api.router,
# Router de usuarios: /users/...
paquetes_api.router,
# Router de productos: /products/...
reservas_api.router,
# Router de órdenes: /orders/...
# Aquí agregas nuevos routers cuando creas más APIs
]