from rest_framework import serializers
from .models import Pais
from indicators.models import IndicadorEconomico
from datetime import datetime


class PaisSerializer(serializers.ModelSerializer):
    """
    Serializer para la gestión de Países con validaciones geográficas.
    """

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

    # --- VALIDACIONES DE NEGOCIO EN ESPAÑOL ---

    def validate_codigo_iso(self, value):
        # Regla: El código ISO debe ser de 2 o 3 caracteres (estándar internacional)
        if not (2 <= len(value) <= 3):
            raise serializers.ValidationError(
                "El código ISO debe tener una longitud de 2 o 3 caracteres (ej: CO o COL)."
            )
        return value.upper()

    def validate_poblacion(self, value):
        # Regla: La población no puede ser negativa
        if value < 0:
            raise serializers.ValidationError(
                "La cantidad de población no puede ser un valor negativo."
            )
        return value

    def validate(self, data):
        """
        Validación de coordenadas geográficas.
        """
        lat = data.get("latitud")
        lon = data.get("longitud")

        if lat is not None and not (-90 <= lat <= 90):
            raise serializers.ValidationError(
                {"latitud": "La latitud debe estar en el rango de -90 a 90 grados."}
            )

        if lon is not None and not (-180 <= lon <= 180):
            raise serializers.ValidationError(
                {"longitud": "La longitud debe estar en el rango de -180 a 180 grados."}
            )

        return data


class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    """
    Serializer para Indicadores con reglas de consistencia económica.
    """

    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    unidad_display = serializers.CharField(source="get_unidad_display", read_only=True)

    class Meta:
        model = IndicadorEconomico
        fields = [
            "tipo",
            "tipo_display",
            "valor",
            "unidad",
            "unidad_display",
            "anio",
            "fuente",
            "fecha_actualizacion",
        ]

    # --- VALIDACIONES DE NEGOCIO EN ESPAÑOL ---

    def validate_anio(self, value):
        anio_actual = datetime.now().year
        # Regla: Evitar datos de un futuro irreal
        if value > anio_actual + 1:
            raise serializers.ValidationError(
                f"No es posible registrar indicadores para el año {value}. El límite es el año siguiente al actual."
            )
        return value

    def validate_valor(self, value):
        # Regla: Ciertos indicadores como Tasa de Desempleo o Inflación no deberían ser incoherentes
        # Aunque permitimos valores negativos para inflación (deflación), limitamos extremos
        if value > 1000000:  # Protección contra errores de dedo masivos
            raise serializers.ValidationError(
                "El valor ingresado excede los rangos históricos permitidos para este indicador."
            )
        return value
