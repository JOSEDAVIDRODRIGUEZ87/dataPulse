from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "pais",
        "tipo_alerta",
        "severidad",
        "leida",
        "fecha_creacion",
    )
    list_filter = ("leida", "severidad", "tipo_alerta", "pais")
    search_fields = ("titulo", "mensaje", "usuario__email")
    # Acciones rápidas para marcar como leídas
    actions = ["marcar_como_leidas"]

    @admin.action(description="Marcar seleccionadas como leídas")
    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
