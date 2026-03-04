from .models import Pais
from exchange_rate.models import TipoCambio
from datetime import datetime
import requests


def obtener_indicadores_pais(moneda_codigo):
    """
    Consulta real a la API de tipos de cambio para obtener el valor del USD.
    """
    try:
        # Usamos una API gratuita de tipos de cambio
        url = f"https://open.er-api.com/v6/latest/USD"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code == 200:
            # Extraemos el valor de la moneda específica (ej: COP, ARS, etc.)
            tasas = data.get("rates", {})
            valor = tasas.get(moneda_codigo.upper(), "N/A")

            return {
                "tipo_cambio_usd": valor,
                "moneda_base": "USD",
                "moneda_destino": moneda_codigo.upper(),
                "actualizado": data.get("time_last_update_utc", "Desconocido"),
                "fuente": "ExchangeRate-API (Real-time data)",
            }
    except Exception as e:
        # Si la API externa falla, devolvemos un mensaje de error controlado
        return {"error": "No se pudo conectar con el servicio económico externo."}

    return {"error": "Datos no disponibles"}


def sincronizar_todos_los_indicadores():
    """
    Lógica para el POST: Recorre todos los países y guarda su tipo de cambio actual.
    """
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, "Error al conectar con la API externa"

        data = response.json()
        tasas = data.get("rates", {})

        # Traemos todos los países de la BD
        paises = Pais.objects.all()
        conteo = 0

        for pais in paises:
            codigo = pais.moneda_codigo
            if codigo and codigo.upper() in tasas:
                # Guardamos o actualizamos el registro de hoy
                TipoCambio.objects.update_or_create(
                    pais=pais,
                    fecha=datetime.now().date(),
                    defaults={
                        "tasa": tasas[codigo.upper()],
                        "moneda_destino": "USD",
                        "fuente": "Sincronización Masiva API",
                        # AGREGAMOS ESTA LÍNEA PARA EVITAR EL ERROR NOT NULL:
                        "variacion_porcentual": 0.0,
                    },
                )
                conteo += 1
        return True, f"Sincronización exitosa: {conteo} países actualizados."
    except Exception as e:
        return False, str(e)
