from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import IndicadorEconomico
from .serializers import IndicadorEconomicoSerializer
from core.pagination import StandardResultsSetPagination


class PaisIndicadoresListView(generics.ListAPIView):
    """
    Lista indicadores filtrados por código ISO de país, con filtros
    y ordenamiento dinámico.
    """

    serializer_class = IndicadorEconomicoSerializer
    pagination_class = StandardResultsSetPagination

    # REQUISITOS TRANSVERSALES: Motores de DRF y Django-Filter
    filter_backends = [
        DjangoFilterBackend,  # Para filtros exactos (?tipo=PIB)
        filters.OrderingFilter,  # Para ordenamiento (?ordering=-valor)
    ]

    # Configuración de Filtros (Query Params)
    # Reemplaza la lógica manual de get_queryset
    filterset_fields = ["tipo", "anio"]

    # Configuración de Ordenamiento
    ordering_fields = ["anio", "valor", "tipo"]
    ordering = ["-anio", "tipo"]  # Orden por defecto

    def get_queryset(self):
        # El parámetro de la URL (codigo_iso) sigue siendo obligatorio
        # para definir el contexto del país.
        codigo = self.kwargs["codigo_iso"].upper()
        return IndicadorEconomico.objects.filter(pais_id=codigo)
