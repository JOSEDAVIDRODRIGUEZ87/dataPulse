from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminRole

from .models import Pais
from .serializers import PaisSerializer

# --- ACTUALIZACIÓN DE IMPORTACIONES ---
from .services import (
    obtener_indicadores_pais,
    sincronizar_todos_los_indicadores,
    sincronizar_indicadores_banco_mundial, 
    sincronizar_perfil_paises_rest,# <-- Nueva función unificada
)
from core.pagination import StandardResultsSetPagination


class PaisListView(generics.ListAPIView):
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["region", "activo"]
    search_fields = ["nombre", "codigo_iso", "moneda_nombre"]
    ordering_fields = ["nombre", "codigo_iso", "region"]
    ordering = ["nombre"]

    def get_queryset(self):
        return Pais.objects.all()


class PaisDetailView(generics.RetrieveAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "codigo_iso"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        pais_data = self.get_serializer(instance).data
        # Esto sigue trayendo el tipo de cambio USD en tiempo real
        indicadores = obtener_indicadores_pais(instance.moneda_codigo)
        return Response(
            {"perfil_pais": pais_data, "indicadores_economicos": indicadores}
        )


class SyncIndicadoresView(APIView):
    """Sincroniza Tipos de Cambio (ExchangeRate API)"""

    permission_classes = [IsAdminRole]

    def post(self, request):
        exito, mensaje = sincronizar_todos_los_indicadores()
        if exito:
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        return Response(
            {"error": mensaje}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# --- NUEVA VISTA PARA EL BANCO MUNDIAL ---
class SyncWorldBankView(APIView):
    """Sincroniza Indicadores Económicos (World Bank API)"""

    permission_classes = [IsAdminRole]

    def post(self, request):
        exito, mensaje = sincronizar_indicadores_banco_mundial()
        if exito:
            return Response(
                {"status": "success", "message": mensaje}, status=status.HTTP_200_OK
            )
        return Response(
            {"status": "error", "message": mensaje},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

class SyncRestCountriesView(APIView):
    """
    Endpoint para sincronizar datos geográficos y básicos de los países.
    """
    permission_classes = [IsAdminRole]

    def post(self, request):
        exito, mensaje = sincronizar_perfil_paises_rest()
        if exito:
            return Response({"status": "success", "message": mensaje}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": mensaje}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)