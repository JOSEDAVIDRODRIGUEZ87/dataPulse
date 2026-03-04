from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class IndicadorEconomico(models.Model):
    # ... (TIPO_CHOICES, UNIDAD_CHOICES y FUENTE_CHOICES se mantienen igual) ...
    TIPO_CHOICES = [
        ("PIB", "Producto Interno Bruto"),
        ("INFLACION", "Inflación"),
        ("DESEMPLEO", "Desempleo"),
        ("BALANZA_COMERCIAL", "Balanza Comercial"),
        ("DEUDA_PIB", "Deuda / PIB"),
        ("PIB_PERCAPITA", "PIB Per Cápita"),
    ]

    UNIDAD_CHOICES = [
        ("PORCENTAJE", "Porcentaje (%)"),
        ("USD", "Dólares (USD)"),
        ("USD_MILES_MILLONES", "Miles de Millones (USD)"),
    ]

    FUENTE_CHOICES = [
        ("WORLD_BANK", "World Bank API"),
        ("MANUAL", "Ingreso Manual"),
    ]

    pais = models.ForeignKey(
        "countries.Pais", on_delete=models.CASCADE, related_name="indicadores"
    )

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=20, decimal_places=4)
    unidad = models.CharField(max_length=20, choices=UNIDAD_CHOICES)

    # Añadimos validación de rango para el año (desde 1900 hasta el actual + 1)
    anio = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year + 1),
        ]
    )

    fuente = models.CharField(max_length=20, choices=FUENTE_CHOICES, default="MANUAL")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Indicador Económico"
        verbose_name_plural = "Indicadores Económicos"
        ordering = ["-anio", "tipo"]

        # Reemplazamos unique_together por UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["pais", "tipo", "anio"], name="unique_indicador_por_pais_anio"
            )
        ]

    def __str__(self):
        # Usamos self.pais_id para evitar consultas extra a la DB
        return f"{self.pais_id} - {self.tipo} ({self.anio})"
