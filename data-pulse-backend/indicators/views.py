from rest_framework import generics
from .models import IndicadorEconomico
from .serializers import IndicadorEconomicoSerializer


class PaisIndicadoresListView(generics.ListAPIView):
    """
    Lista indicadores filtrados por código ISO de país, tipo y año.
    URL: /api/paises/<codigo_iso>/indicadores/?tipo=PIB&anio=2024
    """

    serializer_class = IndicadorEconomicoSerializer

    def get_queryset(self):
        # 1. Capturamos el código del país desde la URL (<str:codigo_iso>)
        # Usamos pais_id porque codigo_iso es la PK del modelo Pais
        codigo = self.kwargs["codigo_iso"].upper()
        queryset = IndicadorEconomico.objects.filter(pais_id=codigo)

        # 2. Capturamos filtros opcionales de la URL (?tipo=...&anio=...)
        tipo = self.request.query_params.get("tipo")
        anio = self.request.query_params.get("anio")

        if tipo:
            queryset = queryset.filter(tipo=tipo.upper())
        if anio:
            queryset = queryset.filter(anio=anio)

        return queryset
