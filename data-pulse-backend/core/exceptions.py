from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # 1. Obtenemos la respuesta base de DRF
    response = exception_handler(exc, context)

    # 2. CASO: Errores no controlados (500 Internal Server Error)
    if response is None:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        return Response(
            {
                "status": "error",
                "code": 500,
                "message": "Ocurrió un error inesperado en el servidor.",
                "details": str(exc),  # Nota: En producción, podrías ocultar str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # 3. CASO: Errores controlados por DRF (400, 401, 403, 404)
    # Definimos mensajes amigables según el código de estado
    messages = {
        400: "La solicitud contiene datos inválidos.",
        401: "No se proporcionaron credenciales de autenticación válidas.",
        403: "No tienes permisos para realizar esta acción.",
        404: "El recurso solicitado no fue encontrado.",
        405: "Método HTTP no permitido.",
        429: "Has superado el límite de peticiones permitidas.",
    }

    # Estructura consistente para el Frontend
    custom_data = {
        "status": "error",
        "code": response.status_code,
        "message": messages.get(response.status_code, "Error en la solicitud"),
        "details": response.data,  # Aquí vendrán los errores de los Serializers
    }

    # 4. Refinamiento opcional: Si el error es una lista de strings, lo simplificamos
    if isinstance(response.data, list) and len(response.data) > 0:
        custom_data["message"] = response.data[0]

    response.data = custom_data
    return response
