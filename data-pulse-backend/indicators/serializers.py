from rest_framework import serializers
from .models import IndicadorEconomico

class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    # Campos calculados para mostrar el texto amigable en lugar del código
    # Ejemplo: En el JSON verás "Producto Interno Bruto" además de "PIB"
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    unidad_display = serializers.CharField(source="get_unidad_display", read_only=True)
    fuente_display = serializers.CharField(source="get_fuente_display", read_only=True)

    class Meta:
        model = IndicadorEconomico
        fields = [
            "id",
            "tipo",
            "tipo_display",
            "valor",
            "unidad",
            "unidad_display",
            "anio",
            "fuente",
            "fuente_display",
            "fecha_actualizacion",
        ]
        # El campo 'pais' no lo incluimos aquí porque ya viene implícito
        # en la URL del endpoint (/paises/CO/indicadores/)
