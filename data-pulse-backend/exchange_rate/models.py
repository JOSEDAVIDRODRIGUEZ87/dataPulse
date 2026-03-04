from django.db import models

class TipoCambio(models.Model):
    # Relacionamos con el País para obtener su moneda_codigo
    # Usamos related_name para consultas inversas como: pais.tipos_de_cambio.all()
    pais = models.ForeignKey(
        'countries.Pais', # <-- IMPORTANTE: Entre comillas 'app.Modelo'
        on_delete=models.CASCADE, 
        related_name='tipos_de_cambio',
        verbose_name="País de Origen"
    )
    
    # moneda_destino: Por defecto "USD" como pide el requerimiento
    moneda_destino = models.CharField(max_length=3, default="USD")
    
    # tasa: Valor del cambio (ej: 3950.50)
    tasa = models.DecimalField(max_digits=18, decimal_places=6)
    
    # fecha: Día del registro
    fecha = models.DateField()
    
    # variacion_porcentual: Respecto al día anterior (ej: -0.05 para una caída del 5%)
    variacion_porcentual = models.DecimalField(
        max_digits=7, 
        decimal_places=4, 
        help_text="Variación respecto al cierre anterior"
    )
    
    # fuente: De dónde viene el dato (Manual, Yahoo Finance, etc.)
    fuente = models.CharField(max_length=100, default="MANUAL")

    class Meta:
        verbose_name = "Tipo de Cambio"
        verbose_name_plural = "Tipos de Cambio"
        # Evita tener dos tasas para el mismo país en la misma fecha
        unique_together = ['pais', 'moneda_destino', 'fecha']
        ordering = ['-fecha']

    def __str__(self):
        # Mostramos moneda_codigo del país relacionado para cumplir con el requerimiento visual
        return f"{self.pais.moneda_codigo} a {self.moneda_destino}: {self.tasa} ({self.fecha})"
    
    @property
    def moneda_origen(self):
        return self.pais.moneda_codigo