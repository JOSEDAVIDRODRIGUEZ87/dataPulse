from django.contrib import admin
from .models import LogActividad


@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "accion", "entidad_afectada", "ip_address")
    list_filter = ("accion", "entidad_afectada", "fecha")
    search_fields = ("usuario__email", "entidad_id", "detalle")
    readonly_fields = (
        "fecha",
        "usuario",
        "accion",
        "entidad_afectada",
        "entidad_id",
        "detalle",
        "ip_address",
    )

    # Seguridad: Un log de auditoría no debería poderse editar ni crear manualmente
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
