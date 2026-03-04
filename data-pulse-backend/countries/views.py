from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminRole

from .models import Pais
from .serializers import PaisSerializer
from .services import obtener_indicadores_pais, sincronizar_todos_los_indicadores
from core.pagination import StandardResultsSetPagination


class PaisListView(generics.ListAPIView):
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # REQUISITOS TRANSVERSALES
    filter_backends = [
        DjangoFilterBackend,  # Filtro exacto (?region=EUROPA)
        filters.SearchFilter,  # Búsqueda textual (?search=Colom)
        filters.OrderingFilter,  # Ordenamiento (?ordering=-nombre)
    ]

    # Configuración de los campos
    filterset_fields = ["region", "activo"]
    search_fields = ["nombre", "codigo_iso", "moneda_nombre"]  # <-- Búsqueda por texto
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
        indicadores = obtener_indicadores_pais(instance.moneda_codigo)
        return Response(
            {"perfil_pais": pais_data, "indicadores_economicos": indicadores}
        )


class SyncIndicadoresView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        exito, mensaje = sincronizar_todos_los_indicadores()
        if exito:
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        return Response(
            {"error": mensaje}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
