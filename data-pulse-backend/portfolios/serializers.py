from rest_framework import serializers
from .models import Portafolio


class PortafolioSerializer(serializers.ModelSerializer):
    """
    Serializer base para Listar y Crear.
    Mantiene la respuesta ligera para el listado general.
    """

    usuario_email = serializers.ReadOnlyField(source="usuario.email")

    class Meta:
        model = Portafolio
        fields = [
            "id",
            "nombre",
            "descripcion",
            "usuario_email",
            "es_publico",
            "activo",
            "fecha_creacion",
            "fecha_modificacion",
        ]

    def create(self, validated_data):
        # El usuario se extrae del contexto enviado por la vista (perform_create)
        # o directamente del request si no se pasa explícitamente.
        return Portafolio.objects.create(**validated_data)


class PortafolioDetalleSerializer(serializers.ModelSerializer):
    """
    Serializer extendido para el Detalle (/api/portafolios/{id}/).
    Incluye cálculos de métricas y (futuras) posiciones.
    """

    usuario_email = serializers.ReadOnlyField(source="usuario.email")

    # Métricas calculadas en tiempo real
    valor_total_usd = serializers.SerializerMethodField()
    rendimiento_porcentual = serializers.SerializerMethodField()
    cantidad_activos = serializers.SerializerMethodField()

    class Meta:
        model = Portafolio
        fields = [
            "id",
            "nombre",
            "descripcion",
            "usuario_email",
            "es_publico",
            "activo",
            "valor_total_usd",
            "rendimiento_porcentual",
            "cantidad_activos",
            "fecha_creacion",
            "fecha_modificacion",
        ]

    def get_valor_total_usd(self, obj):
        """
        Suma el valor actual de todas las posiciones vinculadas.
        """
        # Ejemplo: return sum(p.cantidad * p.precio_actual for p in obj.posiciones.all())
        return 0.0

    def get_rendimiento_porcentual(self, obj):
        """
        Calcula la ganancia/pérdida comparando costo vs valor actual.
        """
        # Ejemplo de lógica:
        # costo = sum(p.cantidad * p.precio_compra for p in obj.posiciones.all())
        # if costo == 0: return "0.00%"
        # valor_actual = self.get_valor_total_usd(obj)
        # return f"{((valor_actual - costo) / costo) * 100:.2f}%"
        return "0.00%"

    def get_cantidad_activos(self, obj):
        """
        Retorna el conteo de activos diferentes en el portafolio.
        """
        if hasattr(obj, "posiciones"):
            return obj.posiciones.count()
        return 0
