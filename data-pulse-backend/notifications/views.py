from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import Alerta
from django.shortcuts import get_object_or_404

from core.pagination import StandardResultsSetPagination


class ListaAlertasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # --- ORDENAMIENTO DINÁMICO ---
        # Permitimos que el frontend ordene por fecha o severidad (?ordering=severidad)
        ordering = request.query_params.get("ordering", "-fecha_creacion")
        allowed_ordering = [
            "fecha_creacion",
            "-fecha_creacion",
            "severidad",
            "-severidad",
        ]

        if ordering not in allowed_ordering:
            ordering = "-fecha_creacion"

        queryset = Alerta.objects.filter(
            Q(usuario=request.user) | Q(usuario__isnull=True)
        ).order_by(ordering)

        # --- FILTROS (Mantenemos tu lógica pero estandarizada) ---
        leida_param = request.query_params.get("leida")
        if leida_param is not None:
            queryset = queryset.filter(leida=leida_param.lower() == "true")

        tipo_param = request.query_params.get("tipo")
        if tipo_param:
            queryset = queryset.filter(tipo_alerta=tipo_param.upper())

        severidad_param = request.query_params.get("severidad")
        if severidad_param:
            queryset = queryset.filter(severidad=severidad_param.upper())

        # --- PAGINACIÓN (Tu implementación manual está perfecta para APIView) ---
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            # 3. Formatear solo los datos de la página actual
            data = [
                {
                    "id": alerta.id,
                    "pais": (
                        alerta.pais.nombre
                        if hasattr(alerta.pais, "nombre")
                        else str(alerta.pais)
                    ),
                    "tipo": alerta.get_tipo_alerta_display(),
                    "severidad": alerta.get_severidad_display(),
                    "titulo": alerta.titulo,
                    "mensaje": alerta.mensaje,
                    "leida": alerta.leida,
                    "fecha": alerta.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
                    "es_global": alerta.usuario is None,
                }
                for alerta in page
            ]
            # 4. Retornar la respuesta con metadatos (count, next, previous)
            return paginator.get_paginated_response(data)

        # Fallback (aunque con PageNumberPagination siempre entra al if anterior)
        return Response({"alertas": []})


class MarcarAlertaLeidaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # 1. Buscar la alerta asegurando que sea del usuario o global
        alerta = get_object_or_404(
            Alerta, Q(pk=pk) & (Q(usuario=request.user) | Q(usuario__isnull=True))
        )

        # 2. Cambiar el estado
        alerta.leida = True
        alerta.save()

        return Response(
            {
                "status": "success",
                "message": f"Alerta {pk} marcada como leída.",
                "id": alerta.id,
                "leida": alerta.leida,
            }
        )


class MarcarTodasLeidasView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # 1. Filtrar las alertas que pertenecen al usuario o son globales
        # y que aún no han sido leídas
        queryset = Alerta.objects.filter(
            Q(usuario=request.user) | Q(usuario__isnull=True), leida=False
        )

        # 2. Contar cuántas se van a marcar (opcional, para el mensaje)
        cantidad = queryset.count()

        # 3. Actualización masiva en la base de datos
        queryset.update(leida=True)

        return Response(
            {
                "status": "success",
                "mensaje": f"Se han marcado {cantidad} alertas como leídas.",
                "conteo_actualizado": cantidad,
            }
        )


class ResumenAlertasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Filtro base: Alertas del usuario o globales
        user_alerts = Alerta.objects.filter(
            Q(usuario=request.user) | Q(usuario__isnull=True)
        )

        # 2. Conteo por Tipo de Alerta
        por_tipo = user_alerts.values("tipo_alerta").annotate(total=Count("id"))

        # 3. Conteo por Severidad
        por_severidad = user_alerts.values("severidad").annotate(total=Count("id"))

        # 4. Conteo específico de No Leídas
        no_leidas = user_alerts.filter(leida=False).count()

        return Response(
            {
                "total_alertas": user_alerts.count(),
                "no_leidas": no_leidas,
                "resumen_por_tipo": {
                    item["tipo_alerta"]: item["total"] for item in por_tipo
                },
                "resumen_por_severidad": {
                    item["severidad"]: item["total"] for item in por_severidad
                },
            }
        )
