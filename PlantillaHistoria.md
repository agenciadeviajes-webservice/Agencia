# '[HU-XXX] EJEMPLO HISTORIAS DE USUARIO '

## 📖 Historia de Usuario

Como 
Quiero
Para

## 🔁 Flujo Esperado

- El usuario obtiene la fecha de proceso desde la interfaz.
- El sistema consume el endpoint /api/v1/cartera/precierre/saldos_consolidados?fecha_proceso=YYYY-MM-DD.
- El backend consulta la base de datos de Réplica filtrando por pCieCarFecCie.
- Se realiza la suma de los valores consolidados para los campos:
- pCieCarSalAct / Capital
- pCieCarIntCau / Intereses causados
- pCieCarIntCon / Intereses contingentes


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET con parámetro fecha_proceso.
- [ ] Se valida que la fecha recibida tenga registros en la tabla preciecar.


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "mensaje": "Consulta de saldos exitosa",
  "data": {
    "fecha_proceso": "2025-07-31",
    "capital_total": 8500000000,
    "intereses_causados": 2400000,
    "intereses_contingentes": 1200000
  },
  "success": true
}
```

- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "No existen datos consolidados para la fecha indicada",
  "data": {
    "fecha_proceso": "2025-07-31",
    "capital_total": 0,
    "intereses_causados": 0,
    "intereses_contingentes": 0
  },
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Consulta del Último Cierre

- **Método HTTP:** `GET`
- **Ruta:** ` /api/v1/cartera/precierre/saldos_consolidados`

## 📤 Ejemplo de Respuesta JSON

````json

```json
{
  "mensaje": "Consulta de saldos exitosa",
  "data": {
    "fecha_proceso": "2025-07-31",
    "capital_total": 8500000000,
    "intereses_causados": 2400000,
    "intereses_contingentes": 1200000
  },
  "success": true
}

````

- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "No existen datos consolidados para la fecha indicada",
  "data": {
    "fecha_proceso": "2025-07-31",
    "capital_total": 0,
    "intereses_causados": 0,
    "intereses_contingentes": 0
  },
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: 

- **Precondición:** La tabla preciecar contiene registros con la fecha de cierre proporcionada (fecha_proceso).
- **Acción:** Ejecutar el endpoint GET /api/v1/cartera/precierre/saldos_consolidados?fecha_proceso=2025-06-30.
- **Resultado esperado:**

  - 
  - 
  - 
  - 

  ### ✅ Caso 2:

- **Precondición:** : La tabla preciecar no contiene registros con la fecha 2025-07-31 (finde mes a procesar).
- **Acción:** Ejecutar el endpoint con GET /api/v1/cartera/precierre/saldos_consolidados?fecha_proceso=2025-07-31.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo capital = 0
  - Campo intereses_causados = 0
  - Campo intereses_contingentes = 0
  - Campo mensaje contiene el texto: "No existen saldos consolidados para la fecha proporcionada"

### ✅ Caso 3: 

- **Precondición:** Ejecución exitosa del endpoint.
- **Resultado esperado:** : La respuesta JSON debe contener exactamente los campos:

  - "capital" (número decimal)
  - "intereses_causados" (número decimal)
  - "intereses_contingentes" (número decimal)
  - "mensaje" (texto)

  ### ❌ Caso 4: 

- **Precondición:** El usuario envía el parámetro fecha_proceso con formato incorrecto (por ejemplo, "30-06-2025").
- **Acción:** Ejecutar el endpoint con GET /api/v1/cartera/precierre/saldos_consolidados?fecha_proceso=30-06-2025.
- **Resultado esperado:**

  - Código HTTP 400 Bad Request
  - Campo `mensaje` contiene un texto descriptivo como: `"No fue posible consultar el último cierre."`
  - Campo mensaje contiene el texto: "Formato de fecha no válido. Debe ser YYYY-MM-DD"

  ### ❌ Caso 5: 

- **Precondición:** La base de datos no está disponible o ocurre un error en la consulta.
- **Acción:** Ejecutar el endpoint bajo condiciones simuladas de fallo de BD.
- **Resultado esperado:**
  - Código HTTP 503 Service Unavailable
  - Campo mensaje contiene el texto: "No fue posible consultar los saldos consolidados"

## ✅ Definición de Hecho

#Historia: Consulta del Último Cierre Procesado

## 📦 Alcance Funcional

- [ ] El endpoint entrega información correctamente en base a la fecha proporcionada
- [ ] Los valores consolidados son exactos y están en formato numérico.
- [ ] La respuesta JSON cumple con el contrato definido.

  ## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para sumar correctamente los saldos.
- [ ] Se cubrieron los casos de error y respuesta sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

  ## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe:

  - Propósito del endpoint
  - Campos de entrada y salida
  - Ejemplo de respuesta exitosa
  - Ejemplo de error

  ## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 500 o 503 cuando no hay conexión a la base de datos.
- [ ] El campo `mensaje` en el JSON incluye un texto amigable y claro para el usuario técnico o frontend.
