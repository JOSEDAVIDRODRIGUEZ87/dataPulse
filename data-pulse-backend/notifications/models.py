from django.db import models
from django.conf import settings


class Alerta(models.Model):
    class TipoAlerta(models.TextChoices):
        RIESGO = "RIESGO", "Riesgo de País"
        TIPO_CAMBIO = "TIPO_CAMBIO", "Variación Tipo de Cambio"
        INDICADOR = "INDICADOR", "Cambio en Indicador"

    class Severidad(models.TextChoices):
        INFO = "INFO", "Informativa"
        WARNING = "WARNING", "Advertencia"
        CRITICAL = "CRITICAL", "Crítica"

    # Relación con Usuario: nullable=True permite alertas globales (para todos)
    # Usamos settings.AUTH_USER_MODEL para mayor flexibilidad
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alertas",
    )

    # Relación con Pais usando string para evitar errores de importación
    pais = models.ForeignKey(
        "countries.Pais", on_delete=models.CASCADE, related_name="alertas"
    )

    tipo_alerta = models.CharField(
        max_length=20, choices=TipoAlerta.choices, default=TipoAlerta.INDICADOR
    )

    severidad = models.CharField(
        max_length=15, choices=Severidad.choices, default=Severidad.INFO
    )

    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        # Usamos pais_id por seguridad y rendimiento como vimos antes
        return f"[{self.severidad}] {self.pais_id}: {self.titulo}"
