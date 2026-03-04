from django.urls import path
from .views import PortafolioListCreateView, PortafolioDetailView, PortafolioResumenView,ExportarPortafolioPDFView
from position.views import (
    PosicionCreateView,
    PosicionDetailView,
)  # Importamos la vista de la otra app

urlpatterns = [
    path("", PortafolioListCreateView.as_view(), name="portafolio-list-create"),
    # El <int:pk> captura el ID de la URL
    path("<int:pk>/", PortafolioDetailView.as_view(), name="portafolio-detail"),
    # NUEVO ENDPOINT:
    path(
        "<int:pk>/posiciones/",
        PosicionCreateView.as_view(),
        name="portafolio-posicion-create",
    ),
    # GET/PUT/PATCH/DELETE: /api/portafolios/3/posiciones/1/
    path(
        "<int:portfolio_pk>/posiciones/<int:pk>/",
        PosicionDetailView.as_view(),
        name="posicion-detail",
    ),
    path(
        "<int:pk>/resumen/", PortafolioResumenView.as_view(), name="portafolio-resumen"
    ),
    path(
        "<int:pk>/export/pdf/",
        ExportarPortafolioPDFView.as_view(),
        name="portafolio-export-pdf",
    ),
]
