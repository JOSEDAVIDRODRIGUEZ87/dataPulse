from django.urls import path
from .views import PosicionDetailView

urlpatterns = [
    path("<int:pk>/", PosicionDetailView.as_view(), name="posicion-detail"),
]
