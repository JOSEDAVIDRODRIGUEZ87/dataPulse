from rest_framework import serializers
from .models import Posicion


class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        # Usamos los nombres EXACTOS de tu modelo:
        fields = [
            "id",
            "pais",
            "tipo_activo",
            "monto_inversion_usd",
            "fecha_entrada",
            "fecha_salida",
            "notas",
        ]
        # 'portafolio' no se incluye aquí porque lo inyectamos en la vista
