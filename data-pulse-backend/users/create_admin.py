import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

# Usamos 'email' porque es tu USERNAME_FIELD
email_admin = 'admin@datapulse.com'

if not User.objects.filter(email=email_admin).exists():
    # Creamos el superusuario usando los campos que definiste en tu modelo
    # 'nombre_completo' es requerido en tu JSON de Postman, así que lo incluimos
    User.objects.create_superuser(
        email=email_admin, 
        nombre_completo='Admin DataPulse', 
        password='Password123*'
    )
    print("Superusuario creado con éxito")
else:
    print("El usuario admin ya existe")