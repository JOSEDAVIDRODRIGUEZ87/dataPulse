from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone
from portfolios.models import Portafolio  # Importamos el modelo padre
from .models import Posicion
from .serializers import PosicionSerializer

from core.pagination import StandardResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class PosicionListView(generics.ListAPIView):
    serializer_class = PosicionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # REQUISITOS TRANSVERSALES
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtros por campos exactos (?tipo_activo=ACCION)
    filterset_fields = ["tipo_activo", "pais"]

    # Búsqueda por texto en campos relacionados
    search_fields = ["pais__nombre", "tipo_activo"]

    # Ordenamiento dinámico (?ordering=-monto_inversion_usd)
    ordering_fields = ["fecha_entrada", "monto_inversion_usd", "fecha_salida"]
    ordering = ["-fecha_entrada"]  # Orden por defecto

    def get_queryset(self):
        portfolio_id = self.kwargs.get("portfolio_pk")
        # Mantenemos la seguridad: Solo posiciones de mis portafolios
        return Posicion.objects.filter(
            portafolio_id=portfolio_id, portafolio__usuario=self.request.user
        ).select_related(
            "pais"
        )  # Optimización: evita N+1 consultas al serializar el país

class PosicionCreateView(generics.CreateAPIView):
    """
    Vista para crear una posición vinculada a un portafolio específico.
    URL: /api/portafolios/<pk>/posiciones/
    """

    serializer_class = PosicionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Obtenemos el ID del portafolio desde la URL
        portafolio_id = self.kwargs.get("pk")

        # 2. Verificamos que el portafolio exista, sea del usuario y esté activo
        portafolio = get_object_or_404(
            Portafolio, id=portafolio_id, usuario=self.request.user, activo=True
        )

        # 3. Guardamos la posición inyectando el portafolio encontrado
        serializer.save(portafolio=portafolio)


class PosicionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, editar o eliminar una posición individual por su ID.
    URL: /api/posiciones/<id>/
    """

    serializer_class = PosicionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # SEGURIDAD: Solo permitimos manipular posiciones de portafolios
        # que pertenezcan al usuario autenticado.
        return Posicion.objects.filter(portafolio__usuario=self.request.user)

    def get_object(self):
        # Validamos que la posición pertenezca al portafolio indicado en la URL
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(
            queryset,
            portafolio_id=self.kwargs["portfolio_pk"],  # ID del portafolio
            pk=self.kwargs["pk"],  # ID de la posición
        )
        return obj

    # PERSONALIZACIÓN DEL DELETE
    def destroy(self, request, *args, **kwargs):
        """
        En lugar de eliminar de la DB, marcamos la fecha de salida.
        """
        instance = self.get_object()

        # Seteamos la fecha actual como fecha de salida
        instance.fecha_salida = timezone.now().date()
        instance.save()

        return Response(
            {
                "message": "Posición cerrada exitosamente",
                "fecha_salida": instance.fecha_salida,
            },
            status=status.HTTP_200_OK,
        )
