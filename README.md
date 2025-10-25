# Sistema de Reservas de Paquetes Turísticos

Bienvenido al repositorio del **Sistema de Reservas de Paquetes Turísticos**, elkin una aplicación web diseñada para gestionar usuarios, paquetes turísticos, reservas y pagos de manera eficiente y segura. Este proyecto incluye tanto el backend con APIs REST como el frontend con paneles de administración y gestión de reservas.

---

## Tabla de Contenidos
- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Flujo de Datos](#flujo-de-datos)
- [Historias de Usuario](#historias-de-usuario)
- [Instalación](#instalación)
- [Endpoints Principales](#endpoints-principales)
- [Pruebas](#pruebas)
- [Licencia](#licencia)

---

## Descripción
El sistema permite a los usuarios registrarse, consultar y reservar paquetes turísticos, realizar pagos y gestionar sus reservas. El administrador puede gestionar usuarios, paquetes y visualizar pagos y reservas en paneles interactivos.

**Funciones principales:**
- Registro e inicio de sesión de usuarios.
- Gestión de paquetes turísticos (crear, actualizar, eliminar, listar).
- Creación, consulta, cancelación y confirmación de reservas.
- Generación y confirmación de pagos.
- Paneles de administración y dashboards de gestión.
- Notificaciones y logs de actividad.

---

## Tecnologías
- **Backend:** Java, Spring Boot, REST API, JWT para autenticación.
- **Frontend:** JSP + JSTL, Bootstrap, HTML5, CSS3.
- **Base de Datos:** MySQL.
- **Servicios externos:** Integración SOAP para bancos, pasarela de pagos.
- **Documentación:** Swagger/OpenAPI.

---

## Estructura del Proyecto
/src
/main
/java -> Código fuente Java (controladores, servicios, repositorios)
/resources -> Configuraciones y archivos estáticos
/webapp -> JSP, CSS, JS
/WEB-INF
/jspf -> Archivos de conexión y utilidades


---

## Flujo de Datos
1. El usuario realiza una acción en el frontend (ej. reservar un paquete).
2. La petición llega al **endpoint correspondiente** del backend.
3. La **capa de servicios** valida la lógica de negocio y reglas.
4. La **capa de dominio** gestiona las entidades.
5. La **capa de repositorio** realiza la persistencia en la base de datos.
6. La respuesta se devuelve en formato **JSON estandarizado**:

```json
{
  "success": true,
  "message": "Operación exitosa",
  "data": {...},
  "error_code": null,
  "details": null
}
```

## Historias de Usuario

Algunas HUs destacadas del proyecto:

| ID   | Historia                          | Responsable    |
|------|----------------------------------|----------------|
| HU01 | Registrar usuario                 | Usuario/Admin |
| HU04 | Listar paquetes turísticos        | Integrante 2  |
| HU05 | Crear nuevo paquete               | Integrante 2  |
| HU08 | Crear reserva                     | Integrante 3  |
| HU12 | Generar solicitud de pago         | Integrante 3  |
| HU25 | Cancelar reserva                  | Integrante 3  |
| HU29 | Consultar disponibilidad          | Integrante 3  |
| HU33 | Panel de administración de paquetes | Integrante 2 |

> Todas las historias incluyen **backend y frontend**, validaciones y manejo de errores según JSON estandarizado.

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/usuario/proyecto-reservas.git
```

Configurar base de datos MySQL:

CREATE DATABASE sistema_trabajos_grado;

Configura las credenciales en WEB-INF/jspf/conexion.jspf.

Levantar el servidor Tomcat y acceder al frontend:

http://localhost:8080/proyecto

## Endpoints Principales

| Método | Ruta                                 | Descripción                  |
|--------|-------------------------------------|-----------------------------|
| POST   | /api/v1/clientes                     | Registrar cliente           |
| GET    | /api/v1/paquetes                     | Listar paquetes             |
| POST   | /api/v1/reservas                     | Crear reserva               |
| POST   | /api/v1/pagos/solicitud              | Generar solicitud de pago   |
| PUT    | /api/v1/pagos/{idReserva}/confirmar | Confirmar pago              |
| DELETE | /api/v1/reservas/{idReserva}        | Cancelar reserva            |

> Todos los endpoints devuelven la respuesta en formato JSON estandarizado con manejo de errores.

---

## Pruebas

Se implementaron casos de prueba funcionales y de integración para:

- Creación, actualización y eliminación de paquetes.
- Registro y gestión de usuarios.
- Reservas y pagos con distintos escenarios (éxito, error de validación, error interno de servidor).
- Logs de auditoría y notificaciones.

---

## Licencia

Este proyecto es de uso académico y no comercial.

