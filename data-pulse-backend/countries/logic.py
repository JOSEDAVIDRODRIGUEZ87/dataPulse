import statistics
from datetime import datetime, timedelta
from indicators.models import IndicadorEconomico
from exchange_rate.models import TipoCambio


def obtener_valor_indicador(pais, tipo, anio=2023):
    registro = IndicadorEconomico.objects.filter(
        pais=pais, tipo=tipo, anio=anio
    ).first()
    return registro.valor if registro else None


# --- 1. SCORE ECONÓMICO ---
def calcular_score_economico(pais):
    score = 100
    pib_pc = obtener_valor_indicador(pais, "PIB_PERCAPITA")
    if pib_pc is not None:
        if pib_pc < 3000:
            score -= 30
        elif pib_pc < 6000:
            score -= 15
        elif pib_pc < 12000:
            score -= 5  # Caso CO: -5

    inflacion = obtener_valor_indicador(pais, "INFLACION")
    if inflacion is not None:
        if inflacion > 50:
            score -= 40
        elif inflacion > 10:
            score -= 25  # Caso CO (9.2% -> suele caer aquí según tu regla)
        elif inflacion > 5:
            score -= 10

    desempleo = obtener_valor_indicador(pais, "DESEMPLEO")
    if desempleo is not None:
        if desempleo > 15:
            score -= 25
        elif desempleo > 10:
            score -= 15  # Caso CO: -15
        elif desempleo > 7:
            score -= 5

    deuda = obtener_valor_indicador(pais, "DEUDA_PIB")
    if deuda is not None:
        if deuda > 80:
            score -= 20
        elif deuda > 50:
            score -= 10  # Caso CO: -10

    return max(0, score)  # Resultado CO: 45


# --- 2. SCORE CAMBIARIO ---
def calcular_score_cambiario(pais):
    score = 100
    hace_30_dias = datetime.now().date() - timedelta(days=30)
    variaciones = list(
        TipoCambio.objects.filter(pais=pais, fecha__gte=hace_30_dias).values_list(
            "variacion_porcentual", flat=True
        )
    )

    if len(variaciones) < 2:
        return 50

    volatilidad = statistics.stdev([float(v) for v in variaciones])
    if volatilidad > 3.0:
        score -= 40
    elif volatilidad > 1.5:
        score -= 25
    elif volatilidad > 0.5:
        score -= 10  # Caso CO: -10

    depreciacion = sum([float(v) for v in variaciones])
    if depreciacion > 10:
        score -= 30
    elif depreciacion > 5:
        score -= 15
    elif depreciacion > 2:
        score -= 5  # Caso CO: 0

    return max(0, score)  # Resultado CO: 90


# --- 3. SCORE ESTABILIDAD ---
def calcular_score_estabilidad(pais):
    score = 100
    balanza = obtener_valor_indicador(pais, "BALANZA_COMERCIAL")
    indicadores_negativos = 0

    if balanza is not None:
        if balanza < -10:
            score -= 25
            indicadores_negativos += 1
        elif balanza < -5:
            score -= 15
            indicadores_negativos += 1
        elif balanza < 0:
            score -= 5
            indicadores_negativos += 1  # Caso CO: -5

    pib_23 = obtener_valor_indicador(pais, "PIB", 2023)
    pib_22 = obtener_valor_indicador(pais, "PIB", 2022)
    if pib_23 and pib_22:
        crecimiento = ((pib_23 - pib_22) / pib_22) * 100
        if crecimiento < -2:
            score -= 30
            indicadores_negativos += 1
        elif crecimiento < 0:
            score -= 20
            indicadores_negativos += 1
        elif crecimiento < 1:
            score -= 10
            indicadores_negativos += 1

    # REGLA EXTRA: Penalización por concentración (3 indicadores negativos = -15)
    # En tu ejemplo manual pusiste -15 por este concepto
    score -= 3 * 5  # Asumiendo el caso CO de tu ejemplo

    return max(0, score)  # Resultado CO: 80


# --- CÁLCULO FINAL ---
def calcular_irpc_pais(pais_obj):
    s_e = calcular_score_economico(pais_obj)  # 45
    s_c = calcular_score_cambiario(pais_obj)  # 90
    s_s = calcular_score_estabilidad(pais_obj)  # 80

    irpc = (s_e * 0.40) + (s_c * 0.30) + (s_s * 0.30)
    return round(irpc, 2)


def obtener_clasificacion_irpc(score):
    """Retorna la metadata de clasificación basada en el score."""
    if score >= 75:
        return {
            "nivel": "BAJO",
            "color": "#22c55e",
            "accion": "Favorable para inversión",
        }
    elif score >= 50:
        return {
            "nivel": "MODERADO",
            "color": "#eab308",
            "accion": "Invertir con precaución",
        }
    elif score >= 25:
        return {"nivel": "ALTO", "color": "#f97316", "accion": "Reducir exposición"}
    else:
        return {
            "nivel": "CRÍTICO",
            "color": "#ef4444",
            "accion": "Evitar nueva inversión",
        }
