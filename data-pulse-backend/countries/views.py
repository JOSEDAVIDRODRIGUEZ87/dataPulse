from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Pais
from .serializers import PaisSerializer
from .services import obtener_indicadores_pais, sincronizar_todos_los_indicadores
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status


# --- VISTA PARA LISTAR (La que ya tienes) ---
class PaisListView(generics.ListAPIView):
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Pais.objects.filter(activo=True)
        region_query = self.request.query_params.get("region")
        if region_query:
            queryset = queryset.filter(region=region_query.upper())
        return queryset


# --- VISTA PARA DETALLE + INDICADORES (Nueva) ---
class PaisDetailView(generics.RetrieveAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "codigo_iso"  # Para que busque por 'CO' en lugar de ID

    def retrieve(self, request, *args, **kwargs):
        # 1. Obtener los datos del país de nuestra DB
        instance = self.get_object()
        pais_data = self.get_serializer(instance).data

        # 2. Llamar al servicio para traer indicadores (Lógica Externa)
        # Usamos la moneda del país que está en nuestra DB
        indicadores = obtener_indicadores_pais(instance.moneda_codigo)

        # 3. Responder con ambos datos unidos
        return Response(
            {"perfil_pais": pais_data, "indicadores_economicos": indicadores}
        )


class SyncIndicadoresView(APIView):
    # Requerimiento: Solo ADMIN
    permission_classes = [IsAdminUser]

    def post(self, request):
        exito, mensaje = sincronizar_todos_los_indicadores()
        if exito:
            return Response({"message": mensaje}, status=status.HTTP_200_OK)
        return Response(
            {"error": mensaje}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
