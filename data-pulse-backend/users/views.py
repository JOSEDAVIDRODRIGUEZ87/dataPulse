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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Usuario creado exitosamente",
                    "user": {"username": user.username, "email": user.email},
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # El método GET para VER el perfil
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # NUEVO: El método PUT para ACTUALIZAR el perfil
    def put(self, request):
        # Pasamos 'instance' para que DRF sepa que es una actualización y no una creación
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Perfil actualizado con éxito", "user": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
