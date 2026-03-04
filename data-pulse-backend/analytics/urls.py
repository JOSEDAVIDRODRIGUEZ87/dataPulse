from django.urls import path
from .views import (
    RankingRiesgoPaisView,
    DetalleRiesgoPaisView,
    HistoricoRiesgoFiltroView,
    CalcularRiesgoMasivoView,
)

urlpatterns = [
    # 1. RUTAS ESTÁTICAS (Deben ir primero)
    path(
        "riesgo/calcular/", CalcularRiesgoMasivoView.as_view(), name="riesgo-calcular"
    ),
    path("riesgo/", RankingRiesgoPaisView.as_view(), name="ranking-riesgo"),
    # 2. RUTAS DINÁMICAS (Deben ir después)
    path(
        "riesgo/<str:codigo_iso>/",
        DetalleRiesgoPaisView.as_view(),
        name="detalle-riesgo-pais",
    ),
    path(
        "riesgo/<str:codigo_iso>/historico/",
        HistoricoRiesgoFiltroView.as_view(),
        name="riesgo-historico-filtro",
    ),
]
