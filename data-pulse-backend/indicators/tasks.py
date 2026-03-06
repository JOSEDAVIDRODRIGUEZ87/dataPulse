from celery import shared_task
import logging

logger = logging.getLogger("indicadores")


@shared_task
def sync_indicadores_economicos():
    # Aquí va tu lógica que discutimos anteriormente
    logger.info("Iniciando sincronización...")
    # ... código de petición a API ...
    return "Sincronización finalizada"
