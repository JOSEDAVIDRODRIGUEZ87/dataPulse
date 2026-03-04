# exchange_rate/urls.py
from django.urls import path
from .views import TipoCambioHistoricoListView

urlpatterns = [
    path('', TipoCambioHistoricoListView.as_view(), name='tipo-cambio-historico'),
]