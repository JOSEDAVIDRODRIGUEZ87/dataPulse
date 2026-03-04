from django.contrib import admin
from .models import IndicadorEconomico

@admin.register(IndicadorEconomico)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('pais', 'tipo', 'valor', 'unidad', 'anio', 'fecha_actualizacion')
    list_filter = ('tipo', 'anio', 'pais', 'fuente')
    search_fields = ('pais__nombre', 'tipo')