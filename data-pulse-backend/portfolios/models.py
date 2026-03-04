from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  # Necesario para lanzar el error


class Portafolio(models.Model):
    # --- CAMPOS REQUERIDOS ---
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portafolios"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    es_publico = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Portafolio"
        verbose_name_plural = "Portafolios"
        ordering = ["-fecha_modificacion"]

        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "nombre"], name="unique_portfolio_name_per_user"
            )
        ]

    # --- RESTRICCIÓN DE ROL (Viewer no crea/edita) ---
    def clean(self):
        """
        Valida que el usuario asociado no sea un Viewer.
        """
        # Nota: Asegúrate de que 'role' y 'VIEWER' coincidan con tu modelo CustomUser
        if hasattr(self.usuario, "role") and self.usuario.role == "VIEWER":
            raise ValidationError(
                {
                    "usuario": f"El usuario {self.usuario.email} tiene nivel de acceso 'Viewer' y no puede gestionar portafolios."
                }
            )

    def save(self, *args, **kwargs):
        # Obligamos a ejecutar la validación de clean() antes de guardar en la DB
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.email}"
