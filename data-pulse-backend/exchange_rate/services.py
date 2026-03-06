# exchange_rate/services.py
from .models import TipoCambio
from django.db.models import Max


def obtener_variacion_cambiaria(pais):
    """
    Calcula la variación porcentual del último registro de tipo de cambio.
    """
    # Obtenemos los dos últimos registros para comparar
    registros = TipoCambio.objects.filter(pais=pais).order_by("-fecha")[:2]

    if len(registros) < 2:
        return 0.0

    actual = float(registros[0].valor)
    anterior = float(registros[1].valor)

    # Fórmula: ((PrecioActual - PrecioAnterior) / PrecioAnterior) * 100
    variacion = ((actual - anterior) / anterior) * 100
    return variacion
