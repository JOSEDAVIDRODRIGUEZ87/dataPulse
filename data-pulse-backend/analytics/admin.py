from django.contrib import admin
from .models import IndiceRiesgo


@admin.register(IndiceRiesgo)
class IndiceRiesgoAdmin(admin.ModelAdmin):
    list_display = ("pais", "nivel_riesgo", "indice_compuesto", "fecha_calculo")
    list_filter = ("nivel_riesgo", "pais", "fecha_calculo")
    search_fields = ("pais__nombre", "nivel_riesgo")
    readonly_fields = (
        "fecha_calculo",
    )  # Normalmente los índices calculados no se editan a mano
