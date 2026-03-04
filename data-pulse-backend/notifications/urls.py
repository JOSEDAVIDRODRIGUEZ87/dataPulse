from django.urls import path
from .views import (
    ListaAlertasView,
    MarcarAlertaLeidaView,
    MarcarTodasLeidasView,
    ResumenAlertasView,
)

urlpatterns = [
    path("alertas/", ListaAlertasView.as_view(), name="lista-alertas"),
    path(
        "alertas/resumen/", ResumenAlertasView.as_view(), name="alertas-resumen"
    ),  # <-- Nueva
    path(
        "alertas/leer-todas/",
        MarcarTodasLeidasView.as_view(),
        name="alertas-leer-todas",
    ),
    path("alertas/<int:pk>/leer/", MarcarAlertaLeidaView.as_view(), name="alerta-leer"),
]
