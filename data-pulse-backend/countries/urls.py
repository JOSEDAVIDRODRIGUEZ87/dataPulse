from django.urls import path, include
from .views import PaisListView, PaisDetailView, SyncIndicadoresView
from indicators.views import PaisIndicadoresListView  # Importamos la nueva vista
from exchange_rate import urls as exchange_urls

urlpatterns = [
    # Esto se convierte en /api/paises/
    path("paises/", PaisListView.as_view(), name="listar-paises"),
    # Esto se convierte en /api/paises/CO/
    path("paises/<str:codigo_iso>/", PaisDetailView.as_view(), name="detalle-pais"),
    path(
        "<str:codigo_iso>/indicadores/",
        PaisIndicadoresListView.as_view(),
        name="pais-indicadores",
    ),
    path("<str:codigo_iso>/tipo-cambio/", include(exchange_urls)),
    path("sync-indicadores/", SyncIndicadoresView.as_view(), name="sync-indicadores"),
]
