from rest_framework import serializers
from .models import Portafolio


class PortafolioSerializer(serializers.ModelSerializer):
    """
    Serializer base para Listar y Crear.
    Incluye validaciones de negocio en español.
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

    # --- VALIDACIONES DE NEGOCIO ---

    def validate_nombre(self, value):
        # Regla: El nombre no puede ser solo números
        if value.isdigit():
            raise serializers.ValidationError(
                "El nombre del portafolio debe contener caracteres alfabéticos, no solo números."
            )
        # Regla: Longitud mínima de seguridad
        if len(value) < 5:
            raise serializers.ValidationError(
                "El nombre es demasiado corto. Proporcione un nombre descriptivo de al menos 5 caracteres."
            )
        return value

    def validate(self, data):
        """
        Validación cruzada de campos.
        """
        # Regla: Un portafolio público debe tener obligatoriamente una descripción
        if data.get("es_publico") and not data.get("descripcion"):
            raise serializers.ValidationError(
                {
                    "descripcion": "Para que un portafolio sea público, debe incluir una descripción detallada de su estrategia."
                }
            )

        return data

    def create(self, validated_data):
        return Portafolio.objects.create(**validated_data)


class PortafolioDetalleSerializer(serializers.ModelSerializer):
    """
    Serializer extendido para el Detalle con métricas.
    """

    usuario_email = serializers.ReadOnlyField(source="usuario.email")
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
        # Lógica de suma de posiciones (ejemplo dinámico)
        return 0.0

    def get_rendimiento_porcentual(self, obj):
        return "0.00%"

    def get_cantidad_activos(self, obj):
        # Usamos el count() de Django si existe la relación
        if hasattr(obj, "posiciones"):
            return obj.posiciones.count()
        return 0


class PortafolioResumenSerializer(serializers.Serializer):
    """
    Utilizado para las métricas de distribución.
    """

    distribucion_pais = serializers.DictField()
    distribucion_tipo_activo = serializers.DictField()
    total_invertido = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={
            "max_digits": "El monto excede el límite permitido por el sistema.",
            "invalid": "El total invertido debe ser un número válido.",
        },
    )
