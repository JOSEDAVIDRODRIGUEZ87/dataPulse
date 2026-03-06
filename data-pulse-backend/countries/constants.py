# countries/constants.py o en el mismo archivo de lógica
PAISES_LATAM_ISO = ["CO", "BR", "MX", "AR", "CL", "PE", "EC", "UY", "PY", "PA"]
# --- MAPEO DE INDICADORES BANCO MUNDIAL ---
WORLD_BANK_INDICATORS = {
    "NY.GDP.MKTP.CD": "PIB",
    "FP.CPI.TOTL.ZG": "INFLACION",
    "SL.UEM.TOTL.ZS": "DESEMPLEO",
    "NE.RSB.GNFS.ZS": "BALANZA_COMERCIAL",
    "GC.DOD.TOTL.GD.ZS": "DEUDA_PIB",
    "NY.GDP.PCAP.CD": "PIB_PERCAPITA",
}

API_CONFIG = {
    "WORLD_BANK": "https://api.worldbank.org/v2",
    "EXCHANGE_RATE": "https://open.er-api.com/v6/latest/USD",
    "REST_COUNTRIES": "https://restcountries.com/v3.1",
}