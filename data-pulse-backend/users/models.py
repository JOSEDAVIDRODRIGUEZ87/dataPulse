from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Importamos el manager creado antes


class User(AbstractUser):
    # Roles definidos para DataPulse
    ADMIN = "ADMIN"
    ANALISTA = "ANALISTA"
    VIEWER = "VIEWER"

    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (ANALISTA, "Analista"),
        (VIEWER, "Visualizador"),
    ]

    # --- REQUERIMIENTOS DE LA PRUEBA ---
    username = None  # Anulamos el campo obligatorio de Django
    email = models.EmailField("Correo electrónico", unique=True)
    nombre_completo = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default=VIEWER)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # --- CAMPOS DE COMPATIBILIDAD ---
    # Usamos 'activo' para la lógica de Django
    @property
    def is_active(self):
        return self.activo

    @is_active.setter
    def is_active(self, value):
        self.activo = value

    # --- CONFIGURACIÓN DE AUTENTICACIÓN ---
    USERNAME_FIELD = "email"  # El email ahora es el ID de login
    REQUIRED_FIELDS = ["nombre_completo"]  # Campos que pide al crear superusuario

    objects = CustomUserManager()  # <--- VÍNCULO VITAL CON EL MANAGER

    def __str__(self):
        return f"{self.email} ({self.rol})"
