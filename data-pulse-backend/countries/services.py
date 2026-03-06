import requests
from datetime import datetime, timedelta
from django.db import transaction

# Importaciones de tus apps
from .models import Pais
from exchange_rate.models import TipoCambio
from indicators.models import IndicadorEconomico
from .constants import WORLD_BANK_INDICATORS, API_CONFIG, PAISES_LATAM_ISO
from notifications.services import ejecutar_sistema_alertas
from notifications.services import ejecutar_sistema_alertas
from exchange_rate.services import obtener_variacion_cambiaria
from notifications.models import (
    Alerta,
)  # Asegúrate de que el nombre de la app sea correcto
from .logic import calcular_irpc_pais  # Tu lógica de cálculo de score


# --- SINCRONIZACIÓN DE TIPOS DE CAMBIO ---
def sincronizar_todos_los_indicadores():
    url = API_CONFIG["EXCHANGE_RATE"]
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, "Error al conectar con la API externa"

        data = response.json()
        tasas = data.get("rates", {})
        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)

        paises = Pais.objects.all()
        conteo = 0

        for pais in paises:
            codigo = pais.moneda_codigo
            if codigo and codigo.upper() in tasas:
                tasa_actual = float(tasas[codigo.upper()])

                # Cálculo de variación
                tasa_ayer_obj = TipoCambio.objects.filter(pais=pais, fecha=ayer).first()
                variacion = 0.0
                if tasa_ayer_obj and tasa_ayer_obj.tasa > 0:
                    variacion = (
                        (tasa_actual - float(tasa_ayer_obj.tasa))
                        / float(tasa_ayer_obj.tasa)
                    ) * 100

                # Guardar Tasa
                TipoCambio.objects.update_or_create(
                    pais=pais,
                    fecha=hoy,
                    defaults={
                        "tasa": tasa_actual,
                        "moneda_destino": "USD",
                        "fuente": "ExchangeRate-API (Sincronización)",
                        "variacion_porcentual": round(variacion, 4),
                    },
                )

                # RECALCULAR IRPC Y ALERTAS
                score = calcular_irpc_pais(pais)
                variacion = obtener_variacion_cambiaria(pais)
                ejecutar_sistema_alertas(pais, score, variacion=variacion)
                conteo += 1

        return True, f"Tasas actualizadas: {conteo} países procesados."
    except Exception as e:
        return False, str(e)


# --- SINCRONIZACIÓN BANCO MUNDIAL ---
def sincronizar_indicadores_banco_mundial():
    paises_objetivo = PAISES_LATAM_ISO
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

            # Tras actualizar indicadores macro, recalculamos IRPC y lanzamos Alerta INFO
            score = calcular_irpc_pais(pais_obj)
            ejecutar_sistema_alertas(pais_obj, score)

        return True, f"Banco Mundial: {conteo_registros} registros sincronizados."
    except Exception as e:
        return False, f"Error WB: {str(e)}"


# --- SINCRONIZACIÓN PERFIL PAÍSES ---
def sincronizar_perfil_paises_rest():
    paises_objetivo = PAISES_LATAM_ISO
    base_url = "https://restcountries.com/v3.1/alpha/{}"
    conteo = 0

    try:
        for iso_code in paises_objetivo:
            response = requests.get(base_url.format(iso_code), timeout=10)
            if response.status_code == 200:
                data = response.json()[0]

                # Manejo de moneda
                currencies = data.get("currencies", {})
                moneda_codigo = list(currencies.keys())[0] if currencies else "N/A"
                moneda_nombre = currencies.get(moneda_codigo, {}).get("name", "N/A")

                Pais.objects.update_or_create(
                    codigo_iso=iso_code,
                    defaults={
                        "nombre": data.get("name", {}).get("common"),
                        "moneda_codigo": moneda_codigo,
                        "moneda_nombre": moneda_nombre,
                        "poblacion": data.get("population", 0),
                        "latitud": data.get("latlng", [0, 0])[0],
                        "longitud": data.get("latlng", [0, 0])[1],
                        "activo": True,
                    },
                )
                conteo += 1
        return True, f"Perfiles actualizados: {conteo} países."
    except Exception as e:
        return False, str(e)


def obtener_indicadores_pais(moneda_codigo):
    """
    Mantiene la compatibilidad con las vistas existentes.
    """
    try:
        url = API_CONFIG["EXCHANGE_RATE"]
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
        return {"error": f"Error de conexión: {str(e)}"}
    return {"error": "Datos no disponibles"}
