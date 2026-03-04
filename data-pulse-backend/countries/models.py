from django.db import models


class Pais(models.Model):
    # Definición de las opciones de región solicitadas
    REGION_CHOICES = [
        ("ANDINA", "Región Andina"),
        ("CONO_SUR", "Cono Sur"),
        ("CENTROAMERICA", "Centroamérica"),
        ("CARIBE", "Caribe"),
    ]

    # codigo_iso (PK): Usamos primary_key=True para que este sea el identificador único
    codigo_iso = models.CharField(
        max_length=2,
        primary_key=True,
        help_text="Código ISO de 2 letras (ej: CO, BR, MX)",
    )

    nombre = models.CharField(max_length=100)

    # Datos de la Moneda
    moneda_codigo = models.CharField(max_length=3, help_text="Ej: COP, BRL, MXN")
    moneda_nombre = models.CharField(max_length=50)

    # Región con el set de opciones predefinido
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default="ANDINA")

    # Coordenadas: DecimalField es el estándar para precisión geográfica
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Población: BigIntegerField para evitar errores con países muy poblados
    poblacion = models.BigIntegerField()

    # Estado del registro
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"
