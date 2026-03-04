from django.contrib import admin
from .models import Portafolio

@admin.register(Portafolio)
class PortafolioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'fecha_creacion', 'es_publico', 'activo')
    list_filter = ('es_publico', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'usuario__email', 'usuario__nombre_completo')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
