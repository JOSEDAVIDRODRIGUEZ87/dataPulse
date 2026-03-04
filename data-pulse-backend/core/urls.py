"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import UserProfileView  # Importas tu vista
from countries.views import PaisDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1. Autenticación y Usuarios
    # Esto busca en users/urls.py. Si ahí tienes path('me/', ...),
    # entonces funciona /api/auth/me/
    path("api/auth/", include("users.urls")),
    # 2. JWT (Login y Refresh)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 3. Países y sus derivados
    # Usamos un solo punto de entrada para países
    path("api/paises/", include("countries.urls")),
    
    #4 Endpoint de Portafolio
    path("api/portafolios/", include("portfolios.urls")),
]
