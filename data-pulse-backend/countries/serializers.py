from rest_framework import serializers
from .models import Pais
from indicators.models import IndicadorEconomico


class PaisSerializer(serializers.ModelSerializer):
    # Esto mostrará el texto amigable de la región (ej: "Región Andina")
    region_display = serializers.CharField(source="get_region_display", read_only=True)

    class Meta:
        model = Pais
        fields = [
            "codigo_iso",
            "nombre",
            "moneda_codigo",
            "moneda_nombre",
            "region",
            "region_display",
            "latitud",
            "longitud",
            "poblacion",
            "activo",
        ]

class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    # Esto mostrará "Producto Interno Bruto" en lugar de "PIB" en el JSON
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    unidad_display = serializers.CharField(source='get_unidad_display', read_only=True)

    class Meta:
        model = IndicadorEconomico
        fields = [
            'tipo', 'tipo_display', 'valor', 'unidad', 
            'unidad_display', 'anio', 'fuente', 'fecha_actualizacion'
        ]
