from django.contrib import admin
from .models import Posicion


@admin.register(Posicion)
class PosicionAdmin(admin.ModelAdmin):
    # Columnas que se verán en el listado principal
    list_display = (
        "id",
        "portafolio",
        "tipo_activo",
        "pais",
        "monto_inversion_usd",
        "fecha_entrada",
        "esta_abierta",
    )

    # Filtros laterales (muy útiles para portafolios grandes)
    list_filter = ("tipo_activo", "portafolio", "pais", "fecha_entrada")

    # Buscador por notas o nombre de portafolio (usa __ para acceder a campos de la FK)
    search_fields = ("notas", "portafolio__nombre")

    # Orden predeterminado (por fecha de entrada descendente)
    ordering = ("-fecha_entrada",)

    # Campo calculado para saber si la posición sigue activa
    def esta_abierta(self, obj):
        return obj.fecha_salida is None

    esta_abierta.boolean = True  # Muestra un icono de check/cross verde/rojo
    esta_abierta.short_description = "¿Abierta?"
