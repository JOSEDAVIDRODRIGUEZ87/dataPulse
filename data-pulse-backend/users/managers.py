from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager personalizado donde el email es el identificador único
    para la autenticación en lugar de nombres de usuario.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo Email debe ser obligatorio")

        # Limpiamos el email (pasa a minúsculas la parte del dominio)
        email = self.normalize_email(email)

        # Creamos la instancia del modelo
        user = self.model(email=email, **extra_fields)

        # Encriptamos la contraseña
        user.set_password(password)

        # Guardamos en la base de datos
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un SuperUser con el email y password dados.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("activo", True)
        extra_fields.setdefault("rol", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
