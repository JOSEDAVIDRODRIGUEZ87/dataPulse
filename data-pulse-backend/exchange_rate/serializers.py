from rest_framework import serializers
from .models import TipoCambio


class TipoCambioSerializer(serializers.ModelSerializer):
    # Usamos la propiedad que extrae la moneda del país relacionado
    moneda_origen = serializers.ReadOnlyField()

    class Meta:
        model = TipoCambio
        fields = [
            "id",
            "moneda_origen",
            "moneda_destino",
            "tasa",
            "fecha",
            "variacion_porcentual",
            "fuente",
        ]
