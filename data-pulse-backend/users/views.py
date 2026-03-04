from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)  # Importar la base de JWT
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
)  # Importar tus serializers


# --- VISTA DE REGISTRO (La que ya tenías) ---
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # El Exception Handler atrapará cualquier error de validación (email duplicado, etc.)
        user = serializer.save()

    # Sobrescribimos la respuesta de éxito para que coincida con tu formato
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        return Response(
            {
                "status": "success",
                "message": "Usuario creado exitosamente",
                "user": {"username": user.username, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )


# --- VISTA DE LOGIN (Nueva) ---
class LoginView(TokenObtainPairView):
    """
    Vista personalizada para el login que utiliza el CustomTokenObtainPairSerializer
    para devolver no solo los tokens, sino también la info del usuario.
    """

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# --- VISTA DE PERFIL ---
class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # Al usar raise_exception=True, DRF lanza la excepción automáticamente
        # y nuestro Core se encarga de enviarla con el formato bonito al cliente.
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Perfil actualizado con éxito", "user": serializer.data}
        )
