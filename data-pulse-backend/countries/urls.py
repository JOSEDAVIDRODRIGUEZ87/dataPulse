from django.urls import path, include
from .views import (
    PaisListView,
    PaisDetailView,
    SyncIndicadoresView,
    SyncWorldBankView, 
    SyncRestCountriesView,# <-- Importamos la nueva vista que creamos
)
from indicators.views import PaisIndicadoresListView
from exchange_rate import urls as exchange_urls

urlpatterns = [
    # --- LISTADO Y DETALLE ---
    path("paises/", PaisListView.as_view(), name="listar-paises"),
    path("paises/<str:codigo_iso>/", PaisDetailView.as_view(), name="detalle-pais"),
    # --- INDICADORES POR PAÍS (Hispanoamérica) ---
    path(
        "<str:codigo_iso>/indicadores/",
        PaisIndicadoresListView.as_view(),
        name="pais-indicadores",
    ),
    # --- TIPOS DE CAMBIO ---
    path("<str:codigo_iso>/tipo-cambio/", include(exchange_urls)),
    # --- PROCESOS DE SINCRONIZACIÓN (SOLO ADMIN) ---
    # Sincroniza tasas de cambio USD (ExchangeRate API)
    path("sync-tasas/", SyncIndicadoresView.as_view(), name="sync-indicadores"),
    # Sincroniza indicadores históricos 2019-2023 (World Bank API)
    path("sync-worldbank/", SyncWorldBankView.as_view(), name="sync-worldbank"),
    
    path("sync-perfil/", SyncRestCountriesView.as_view(), name="sync-perfil-paises"),
]
