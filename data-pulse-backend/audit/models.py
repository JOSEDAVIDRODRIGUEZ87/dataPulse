from django.db import models
from django.conf import settings


class LogActividad(models.Model):
    class Accion(models.TextChoices):
        CREAR = "CREAR", "Crear"
        EDITAR = "EDITAR", "Editar"
        ELIMINAR = "ELIMINAR", "Eliminar"
        CONSULTAR = "CONSULTAR", "Consultar"
        LOGIN = "LOGIN", "Inicio de Sesión"
        EXPORT = "EXPORT", "Exportación de Datos"

    # Usuario que realizó la acción. SET_NULL mantiene el log si el usuario es borrado.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_actividad",
    )

    accion = models.CharField(max_length=20, choices=Accion.choices)

    # Nombre de la tabla o modelo afectado (ej: 'Pais', 'IndicadorEconomico')
    entidad_afectada = models.CharField(max_length=100)

    # ID del registro (usamos CharField para soportar UUIDs o códigos ISO como 'CO')
    entidad_id = models.CharField(max_length=255, null=True, blank=True)

    # Almacena valores antiguos vs nuevos o metadata adicional
    detalle = models.JSONField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Actividad"
        verbose_name_plural = "Logs de Actividad"
        ordering = ["-fecha"]

    def __str__(self):
        user = self.usuario.email if self.usuario else "Sistema"
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M')} - {user} - {self.accion}"
