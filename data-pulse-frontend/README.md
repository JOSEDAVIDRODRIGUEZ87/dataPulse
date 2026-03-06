# DataPulse 🚀

Plataforma de gestión de datos y métricas en tiempo real, diseñada bajo una arquitectura desacoplada para garantizar escalabilidad, seguridad y alto rendimiento.

---

## 1. Arquitectura de la Solución
El sistema sigue un patrón **Cliente-Servidor desacoplado**, donde el frontend (SPA) interactúa de forma asíncrona con el backend a través de una API REST.



* **Frontend:** Angular v21+ (SPA).
* **Backend:** Django REST Framework (DRF).
* **Base de Datos:** PostgreSQL.
* **Orquestación:** Docker & Docker Compose.

## 2. Modelo de Datos (DER)


## 3. Decisiones Técnicas
* **Angular:** Elegido por su robustez, tipado estricto y excelente gestión de servicios HTTP, ideal para aplicaciones empresariales.
* **Django REST Framework:** Seleccionado por su madurez, seguridad integrada (CSRF, autenticación) y la eficiencia de su ORM.
* **Bootstrap 5:** Implementado para garantizar una interfaz responsiva, limpia y de rápida implementación.
* **Docker:** Utilizado para estandarizar el entorno de desarrollo y asegurar paridad entre entornos (local vs. producción).

---

## 4. Guía de Instalación Local
Para ejecutar el proyecto, asegúrate de tener [Docker](https://www.docker.com/) instalado.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/JOSEDAVIDRODRIGUEZ87/dataPulse.git](https://github.com/JOSEDAVIDRODRIGUEZ87/dataPulse.git)
   cd dataPulse