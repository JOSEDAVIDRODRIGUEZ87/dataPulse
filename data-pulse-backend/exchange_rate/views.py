from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TipoCambio
from .serializers import TipoCambioSerializer
from core.pagination import StandardResultsSetPagination


class TipoCambioHistoricoListView(generics.ListAPIView):
    serializer_class = TipoCambioSerializer
    pagination_class = StandardResultsSetPagination

    # REQUISITOS TRANSVERSALES
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Definimos los filtros automáticos
    # Esto reemplaza los 'if fecha_desde' manuales
    filterset_fields = {
        "fecha": [
            "gte",
            "lte",
        ],  # Crea automáticamente ?fecha__gte=... y ?fecha__lte=...
    }

    # Campos por los que el usuario puede ordenar
    ordering_fields = ["fecha", "tasa"]
    ordering = ["-fecha"]  # Orden por defecto

    def get_queryset(self):
        # Mantenemos solo la lógica de filtrado por la URL (codigo_iso)
        # porque es un parámetro estructural, no un query param opcional.
        codigo = self.kwargs["codigo_iso"].upper()
        return TipoCambio.objects.filter(pais_id=codigo)
