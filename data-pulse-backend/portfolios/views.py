from rest_framework import generics, status 
from rest_framework.response import Response # <--- ESTA ES LA LÍNEA QUE FALTA
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import Portafolio
from .serializers import PortafolioSerializer, PortafolioDetalleSerializer


class PortafolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortafolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Portafolio.objects.filter(
            (Q(usuario=user) | Q(es_publico=True)), activo=True
        ).distinct()

    def perform_create(self, serializer):
        try:
            serializer.save(usuario=self.request.user)
        except ValidationError as e:
            raise DRFValidationError(e.message_dict)


# CAMBIO AQUÍ: Heredamos de RetrieveUpdateDestroyAPIView
class PortafolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Si el usuario va a editar (PUT/PATCH), usamos el serializer básico.
        # Si solo va a ver (GET), usamos el de detalle con métricas.
        if self.request.method in ["PUT", "PATCH"]:
            return PortafolioSerializer
        return PortafolioDetalleSerializer

    def get_queryset(self):
        user = self.request.user

        # LÓGICA DE SEGURIDAD:
        # Si es una acción de escritura (PUT, PATCH, DELETE): Solo mis portafolios.
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return Portafolio.objects.filter(usuario=user, activo=True)

        # Si es lectura (GET): Mis portafolios O los públicos.
        return Portafolio.objects.filter(
            Q(usuario=user) | Q(es_publico=True), activo=True
        )

    def perform_update(self, serializer):
        try:
            # Al actualizar, el modelo ejecutará full_clean() y validará si es VIEWER
            serializer.save()
        except ValidationError as e:
            raise DRFValidationError(e.message_dict)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescribimos para devolver un mensaje personalizado
        en lugar de solo el 204 estándar.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"El portafolio '{instance.nombre}' ha sido eliminado correctamente."
            },
            status=status.HTTP_200_OK,  # O HTTP_204_NO_CONTENT si prefieres el estándar
        )

    def perform_destroy(self, instance):
        """
        Esta es la clave del Soft Delete:
        No borramos el objeto, solo cambiamos su estado.
        """
        instance.activo = False
        instance.save()
