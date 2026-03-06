from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# --- SERIALIZER DE REGISTRO ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "La contraseña es muy corta. Debe tener al menos 8 caracteres."
        },
    )
    confirm_password = serializers.CharField(write_only=True, required=True) # Asegura el required=True

    class Meta:
        model = User
        fields = [
            "nombre_completo",  # Cambiado de username por consistencia con tu modelo
            "email",
            "password",
            "confirm_password",
            "rol",
        ]

    def validate_email(self, value):
        # Validación de negocio: Evitar duplicados con mensaje claro
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya se encuentra registrado en nuestra plataforma."
            )
        return value

    def validate(self, attrs):
        # Validación de negocio: Comparación de campos
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Las contraseñas ingresadas no coinciden. Inténtelo de nuevo."
                }
            )

        # Validación de negocio: Restricción de rol ADMIN en el registro público
        if attrs.get("rol") == User.ADMIN:
            raise serializers.ValidationError(
                {
                    "rol": "No está permitido registrarse como Administrador directamente."
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# --- SERIALIZER DE LOGIN ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "No se encontró ninguna cuenta activa con las credenciales proporcionadas."
    }

    def validate(self, attrs):
        # super().validate(attrs) ya maneja el error 401 si las credenciales fallan
        data = super().validate(attrs)

        # Personalizamos la respuesta de éxito
        data["user"] = {
            "id": self.user.id,
            "nombre": self.user.nombre_completo,
            "email": self.user.email,
            "rol": self.user.rol,
        }
        return data


# --- SERIALIZER DE PERFIL/USUARIO ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nombre_completo", "email", "rol", "fecha_creacion"]
        read_only_fields = [
            "id",
            "email",
            "fecha_creacion",
        ]  # El email no debería cambiarse por perfil

    def validate_nombre_completo(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre debe ser real y contener al menos 3 caracteres."
            )
        return value
