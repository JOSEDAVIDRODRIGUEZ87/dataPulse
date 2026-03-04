from django.contrib import admin
from .models import TipoCambio

@admin.register(TipoCambio)
class TipoCambioAdmin(admin.ModelAdmin):
    list_display = ('get_moneda', 'moneda_destino', 'tasa', 'fecha', 'variacion_porcentual', 'fuente')
    list_filter = ('pais', 'fecha', 'fuente')
    search_fields = ('pais__moneda_codigo', 'pais__nombre')

    # Método para mostrar la moneda del país en la lista del admin
    def get_moneda(self, obj):
        return obj.pais.moneda_codigo
    get_moneda.short_description = 'Moneda Origen'