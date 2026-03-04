from django.db import models
from django.core.exceptions import ValidationError


class Posicion(models.Model):
    class TipoActivo(models.TextChoices):
        RENTA_FIJA = "RENTA_FIJA", "Renta Fija"
        RENTA_VARIABLE = "RENTA_VARIABLE", "Renta Variable"
        COMMODITIES = "COMMODITIES", "Commodities"
        MONEDA = "MONEDA", "Moneda"

    # Referencia a la app 'portfolio' (ajustar si la carpeta tiene otro nombre)
    portafolio = models.ForeignKey(
        "portfolios.Portafolio",  # <--- El nombre antes del punto es el nombre de la CARPETA
        on_delete=models.CASCADE,
        related_name="posiciones",
    )

    # Referencia a la app 'countries' (ajustar si la carpeta tiene otro nombre)
    pais = models.ForeignKey(
        "countries.Pais", on_delete=models.PROTECT, related_name="posiciones"
    )

    tipo_activo = models.CharField(
        max_length=20, choices=TipoActivo.choices, default=TipoActivo.RENTA_VARIABLE
    )

    # Corregido: decimal_places
    monto_inversion_usd = models.DecimalField(max_digits=18, decimal_places=2)

    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"

    def clean(self):
        if self.fecha_salida and self.fecha_salida < self.fecha_entrada:
            raise ValidationError(
                "La fecha de salida no puede ser anterior a la fecha de entrada."
            )

    def __str__(self):
        # Usamos self.pais.codigo_iso porque Pais usa ese campo como PK
        return f"{self.tipo_activo} - {self.pais_id} ({self.monto_inversion_usd} USD)"
