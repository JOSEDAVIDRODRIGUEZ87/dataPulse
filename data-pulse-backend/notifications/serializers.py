# notifications/serializers.py
from rest_framework import serializers
from .models import Alerta

class AlertaSerializer(serializers.ModelSerializer):
    # Campos calculados para que el frontend reciba datos amigables
    pais_nombre = serializers.CharField(source='pais.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_alerta_display', read_only=True)
    severidad_display = serializers.CharField(source='get_severidad_display', read_only=True)
    es_global = serializers.SerializerMethodField()
    fecha_formateada = serializers.SerializerMethodField()

    class Meta:
        model = Alerta
        fields = [
            'id', 
            'pais_nombre', 
            'tipo_display', 
            'severidad_display', 
            'titulo', 
            'mensaje', 
            'leida', 
            'fecha_formateada', 
            'es_global'
        ]

    def get_es_global(self, obj):
        """Devuelve True si la alerta es para todos los usuarios."""
        return obj.usuario is None

    def get_fecha_formateada(self, obj):
        """Formato consistente para el frontend."""
        return obj.fecha_creacion.strftime("%Y-%m-%d %H:%M")