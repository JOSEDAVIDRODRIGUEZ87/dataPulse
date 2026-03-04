from rest_framework import generics
from .models import TipoCambio
from .serializers import TipoCambioSerializer


class TipoCambioHistoricoListView(generics.ListAPIView):
    serializer_class = TipoCambioSerializer

    def get_queryset(self):
        # 1. Obtenemos el código ISO de la URL (ej: 'CO')
        codigo = self.kwargs["codigo_iso"].upper()

        # 2. Empezamos filtrando por ese país
        queryset = TipoCambio.objects.filter(pais_id=codigo)

        # 3. Filtro por rango de fechas: ?desde=2024-01-01&hasta=2024-03-01
        fecha_desde = self.request.query_params.get("desde")
        fecha_hasta = self.request.query_params.get("hasta")

        if fecha_desde:
            # __gte: Greater Than or Equal (>=)
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            # __lte: Less Than or Equal (<=)
            queryset = queryset.filter(fecha__lte=fecha_hasta)

        return queryset
