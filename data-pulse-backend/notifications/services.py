from .models import Alerta
from indicators.models import IndicadorEconomico


def ejecutar_sistema_alertas(
    pais_obj, irpc_actual, irpc_anterior=None, variacion_cambio=0.0
):
    """
    Motor de reglas 6 a 10.
    """

    # --- REGLA 6: CRITICAL - IRPC < 25 ---
    if irpc_actual < 25:
        Alerta.objects.create(
            pais=pais_obj,
            tipo_alerta=Alerta.TipoAlerta.RIESGO,
            severidad=Alerta.Severidad.CRITICAL,
            titulo="RIESGO PAÍS CRÍTICO",
            mensaje=f"El IRPC ha caído a {irpc_actual}. El país se encuentra en zona de alto riesgo.",
        )

    # --- REGLA 7: WARNING - Caída > 15 puntos ---
    if irpc_anterior is not None:
        if (irpc_anterior - irpc_actual) > 15:
            Alerta.objects.create(
                pais=pais_obj,
                tipo_alerta=Alerta.TipoAlerta.RIESGO,
                severidad=Alerta.Severidad.WARNING,
                titulo="Deterioro Rápido de Riesgo",
                mensaje=f"El IRPC cayó de {irpc_anterior} a {irpc_actual} puntos bruscamente.",
            )

    # --- REGLA 8: WARNING - Variación Cambio > 3% ---
    if abs(variacion_cambio) > 3.0:
        Alerta.objects.create(
            pais=pais_obj,
            tipo_alerta=Alerta.TipoAlerta.TIPO_CAMBIO,
            severidad=Alerta.Severidad.WARNING,
            titulo="Volatilidad Cambiaria",
            mensaje=f"Se detectó una variación del {round(variacion_cambio, 2)}% en el tipo de cambio.",
        )

    # --- REGLA 10: CRITICAL - Inflación > 50% ---
    # Buscamos el último dato de inflación guardado
    inflacion = (
        IndicadorEconomico.objects.filter(pais=pais_obj, tipo="INFLACION")
        .order_by("-anio")
        .first()
    )
    if inflacion and inflacion.valor > 50:
        Alerta.objects.get_or_create(  # Usamos get_or_create para evitar duplicar alertas de inflación iguales
            pais=pais_obj,
            tipo_alerta=Alerta.TipoAlerta.INDICADOR,
            severidad=Alerta.Severidad.CRITICAL,
            titulo="Hiperinflación Detectada",
            mensaje=f"Inflación superior al 50% ({inflacion.valor}%). Inestabilidad monetaria severa.",
        )

    # --- REGLA 9: INFO - Sincronización Exitosa ---
    Alerta.objects.create(
        pais=pais_obj,
        tipo_alerta=Alerta.TipoAlerta.INDICADOR,
        severidad=Alerta.Severidad.INFO,
        titulo="Sincronización de Datos",
        mensaje=f"Indicadores actualizados correctamente. Nuevo IRPC: {irpc_actual}.",
    )
