import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'david.rodriguez@correo.com', 'demo1234')
    print("Superusuario creado con éxito")
else:
    print("El usuario ya existe")