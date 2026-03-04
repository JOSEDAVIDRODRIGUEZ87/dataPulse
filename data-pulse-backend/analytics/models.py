from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class IndiceRiesgo(models.Model):
    class NivelRiesgo(models.TextChoices):
        BAJO = "BAJO", "Bajo"
        MODERADO = "MODERADO", "Moderado"
        ALTO = "ALTO", "Alto"
        CRITICO = "CRITICO", "Crítico"

    pais = models.ForeignKey(
        "countries.Pais", on_delete=models.CASCADE, related_name="indices_riesgo"
    )

    fecha_calculo = models.DateTimeField(auto_now_add=True)

    score_economico = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    score_cambiario = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    score_estabilidad = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    indice_compuesto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    nivel_riesgo = models.CharField(
        max_length=15, choices=NivelRiesgo.choices, default=NivelRiesgo.MODERADO
    )

    detalle_calculo = models.JSONField(
        help_text="Desglose detallado de los factores de cálculo", null=True, blank=True
    )

    class Meta:
        verbose_name = "Índice de Riesgo"
        verbose_name_plural = "Índices de Riesgo"
        ordering = ["-fecha_calculo"]
        get_latest_by = "fecha_calculo"
        # HEMOS QUITADO EL BLOQUE DE CONSTRAINTS PARA EVITAR EL ERROR DE TIPO

    def __str__(self):
        return f"Riesgo {self.pais} - {self.nivel_riesgo}"
