from .models import Pais
from exchange_rate.models import TipoCambio
from indicators.models import IndicadorEconomico
from datetime import (
    datetime,
    timedelta,
)  # Añadimos timedelta para buscar el día anterior
import requests

# --- MAPEO DE INDICADORES BANCO MUNDIAL ---
WORLD_BANK_INDICATORS = {
    "NY.GDP.MKTP.CD": "PIB",
    "FP.CPI.TOTL.ZG": "INFLACION",
    "SL.UEM.TOTL.ZS": "DESEMPLEO",
    "NE.RSB.GNFS.ZS": "BALANZA_COMERCIAL",
    "GC.DOD.TOTL.GD.ZS": "DEUDA_PIB",
    "NY.GDP.PCAP.CD": "PIB_PERCAPITA",
}


def obtener_indicadores_pais(moneda_codigo):
    try:
        url = f"https://open.er-api.com/v6/latest/USD"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
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
        return {"error": "No se pudo conectar con el servicio económico externo."}
    return {"error": "Datos no disponibles"}


def sincronizar_todos_los_indicadores():
    """
    Actualizado: Consulta ExchangeRate-API y calcula la variación diaria
    comparando con el registro del día anterior en la BD.
    """
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, "Error al conectar con la API externa"

        data = response.json()
        tasas = data.get("rates", {})

        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)  # Fecha para buscar el registro histórico

        paises = Pais.objects.all()
        conteo = 0

        for pais in paises:
            codigo = pais.moneda_codigo
            if codigo and codigo.upper() in tasas:
                tasa_actual = float(tasas[codigo.upper()])

                # --- LÓGICA DE VARIACIÓN DIARIA ---
                # Buscamos si existe una tasa guardada del día anterior
                tasa_ayer_obj = TipoCambio.objects.filter(pais=pais, fecha=ayer).first()

                variacion = 0.0
                if tasa_ayer_obj and tasa_ayer_obj.tasa > 0:
                    tasa_ayer = float(tasa_ayer_obj.tasa)
                    # Fórmula: ((Actual - Anterior) / Anterior) * 100
                    variacion = ((tasa_actual - tasa_ayer) / tasa_ayer) * 100

                TipoCambio.objects.update_or_create(
                    pais=pais,
                    fecha=hoy,
                    defaults={
                        "tasa": tasa_actual,
                        "moneda_destino": "USD",
                        "fuente": "ExchangeRate-API (Sincronización)",
                        "variacion_porcentual": round(
                            variacion, 4
                        ),  # Guardamos la variación calculada
                    },
                )
                conteo += 1
        return (
            True,
            f"Sincronización exitosa: {conteo} países actualizados con cálculo de variación.",
        )
    except Exception as e:
        return False, str(e)


def sincronizar_indicadores_banco_mundial():
    paises_objetivo = ["CO", "BR", "MX", "AR", "CL", "PE", "EC", "UY", "PY", "PA"]
    date_range = "2019:2023"
    base_url = (
        "https://api.worldbank.org/v2/country/{}/indicator/{}?date={}&format=json"
    )
    conteo_registros = 0

    try:
        for code_iso in paises_objetivo:
            pais_obj = Pais.objects.filter(codigo_iso=code_iso).first()
            if not pais_obj:
                continue

            for wb_code, db_type in WORLD_BANK_INDICATORS.items():
                url = base_url.format(code_iso, wb_code, date_range)
                response = requests.get(url, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1 and data[1]:
                        for entry in data[1]:
                            if entry.get("value") is not None:
                                IndicadorEconomico.objects.update_or_create(
                                    pais=pais_obj,
                                    tipo=db_type,
                                    anio=entry.get("date"),
                                    defaults={
                                        "valor": entry.get("value"),
                                        "fuente": "World Bank API",
                                        "fecha_actualizacion": datetime.now(),
                                    },
                                )
                                conteo_registros += 1
        return True, f"Banco Mundial: {conteo_registros} registros sincronizados."
    except Exception as e:
        return False, f"Error WB: {str(e)}"


def sincronizar_perfil_paises_rest():
    """
    Consume REST Countries API para actualizar la información básica de los 10 países.
    """
    paises_objetivo = ["CO", "BR", "MX", "AR", "CL", "PE", "EC", "UY", "PY", "PA"]
    base_url = "https://restcountries.com/v3.1/alpha/{}"
    conteo = 0

    try:
        for iso_code in paises_objetivo:
            url = base_url.format(iso_code)
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()[0]  # La API devuelve una lista con un objeto

                # Extracción de datos con manejo de seguridad (get)
                nombre_oficial = data.get("name", {}).get("official", "N/A")
                poblacion = data.get("population", 0)
                coordenadas = data.get("latlng", [0.0, 0.0])
                bandera_url = data.get("flags", {}).get("png", "")

                # Manejo de moneda (viene como diccionario dinámico: {"COP": {"name": "...", "symbol": "..."}})
                currencies = data.get("currencies", {})
                moneda_codigo = list(currencies.keys())[0] if currencies else "N/A"
                moneda_nombre = currencies.get(moneda_codigo, {}).get("name", "N/A")

                # Actualización en nuestra base de datos
                # Asegúrate de que tu modelo Pais tenga estos campos (latitud, longitud, bandera_url, etc.)
                Pais.objects.update_or_create(
                    codigo_iso=iso_code,
                    defaults={
                        "nombre": data.get("name", {}).get("common", nombre_oficial),
                        "moneda_codigo": moneda_codigo,
                        "moneda_nombre": moneda_nombre,
                        "poblacion": poblacion,
                        "latitud": coordenadas[0],
                        "longitud": coordenadas[1],
                        # "bandera_url": bandera_url, # Agrega este campo a tu modelo si es necesario
                        "activo": True,
                    },
                )
                conteo += 1

        return True, f"Perfiles de países actualizados: {conteo} países procesados."
    except Exception as e:
        return False, f"Error en REST Countries Sync: {str(e)}"
