from rest_framework import serializers
from .models import Pais
from indicators.models import IndicadorEconomico
from datetime import datetime
from .logic import calcular_irpc_pais, obtener_clasificacion_irpc


class PaisSerializer(serializers.ModelSerializer):
    irpc_detalle = serializers.SerializerMethodField()
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
            "irpc_detalle",  # <-- FALTA AGREGAR ESTO PARA QUE SE MUESTRE
        ]

    def get_irpc_detalle(self, obj):
        score = calcular_irpc_pais(obj)
        clasificacion = obtener_clasificacion_irpc(score)
        return {"score": score, **clasificacion}

    # ... (Tus validaciones de Pais están perfectas, no las toqué) ...


class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    unidad_display = serializers.CharField(source="get_unidad_display", read_only=True)

    class Meta:
        model = IndicadorEconomico
        fields = [
            "pais",  # <-- Asegúrate de incluir el país para poder crear indicadores
            "tipo",
            "tipo_display",
            "valor",
            "unidad",
            "unidad_display",
            "anio",
            "fuente",
            "fecha_actualizacion",
        ]

    def validate_anio(self, value):
        anio_actual = datetime.now().year
        if value > anio_actual + 1:
            raise serializers.ValidationError(
                f"No es posible registrar indicadores para el año {value}."
            )
        return value

    def validate_valor(self, value):
        if value > 1000000:
            raise serializers.ValidationError("El valor excede los rangos permitidos.")
        return value

    # --- NUEVA LÓGICA: DISPARAR ALERTAS AL GUARDAR ---
    def create(self, validated_data):
        # Guardamos el indicador
        indicador = super().create(validated_data)

        # Importación local para evitar errores circulares
        from .services import ejecutar_sistema_alertas

        # Recalculamos score y evaluamos alertas (Reglas 6, 9 y 10)
        pais = indicador.pais
        nuevo_score = calcular_irpc_pais(pais)

        # Disparamos el motor de alertas automático
        ejecutar_sistema_alertas(pais, nuevo_score)

        return indicador
