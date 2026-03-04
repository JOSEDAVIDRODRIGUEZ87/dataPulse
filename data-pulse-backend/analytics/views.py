import random
from django.db import transaction, models
from django.db.models import Q, Max, Avg, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Importaciones de modelos
from countries.models import Pais
from notifications.models import Alerta
from portfolios.models import Portafolio
from .models import IndiceRiesgo

from django.db.models.functions import ExtractYear
from core.pagination import StandardResultsSetPagination


# 1. CLASE PARA EL RANKING GENERAL
class RankingRiesgoPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ordering = request.query_params.get("ordering", "-indice_compuesto")
        allowed_ordering = [
            "indice_compuesto",
            "-indice_compuesto",
            "pais__nombre",
            "-pais__nombre",
            "fecha_calculo",
        ]
        if ordering not in allowed_ordering:
            ordering = "-indice_compuesto"

        # 1. Obtener el queryset base
        indices = IndiceRiesgo.objects.select_related("pais").order_by(ordering)

        # 2. Instanciar el paginador
        paginator = StandardResultsSetPagination()

        # 3. Paginar el queryset
        page = paginator.paginate_queryset(indices, request)

        if page is not None:
            # 4. Construir la data solo para los elementos de la página actual
            data = [
                {
                    "pais": (
                        item.pais.nombre
                        if hasattr(item.pais, "nombre")
                        else str(item.pais)
                    ),
                    "indice_riesgo": item.indice_compuesto,
                    "nivel": item.get_nivel_riesgo_display(),
                    "scores": {
                        "economico": item.score_economico,
                        "cambiario": item.score_cambiario,
                        "estabilidad": item.score_estabilidad,
                    },
                    "actualizado_el": item.fecha_calculo.strftime("%Y-%m-%d"),
                }
                for item in page
            ]
            # 5. Devolver respuesta con metadatos (count, next, previous)
            return paginator.get_paginated_response(data)

        # Fallback en caso de que la paginación no se aplique
        return Response([])


# 2. CLASE PARA EL DETALLE E HISTÓRICO
class DetalleRiesgoPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo_iso):
        historico_queryset = (
            IndiceRiesgo.objects.filter(pais__codigo_iso=codigo_iso.upper())
            .select_related("pais")
            .order_by("-fecha_calculo")
        )

        if not historico_queryset.exists():
            return Response(
                {"error": f"No se encontraron datos para el país: {codigo_iso}"},
                status=404,
            )

        actual = historico_queryset[0]
        return Response(
            {
                "pais": (
                    actual.pais.nombre
                    if hasattr(actual.pais, "nombre")
                    else str(actual.pais)
                ),
                "codigo_iso": codigo_iso.upper(),
                "estado_actual": {
                    "indice": actual.indice_compuesto,
                    "nivel": actual.get_nivel_riesgo_display(),
                    "fecha": actual.fecha_calculo.strftime("%Y-%m-%d %H:%M"),
                    "scores": {
                        "economico": actual.score_economico,
                        "cambiario": actual.score_cambiario,
                        "estabilidad": actual.score_estabilidad,
                    },
                },
                "historico": [
                    {
                        "fecha": h.fecha_calculo.strftime("%Y-%m-%d"),
                        "indice": h.indice_compuesto,
                        "nivel": h.get_nivel_riesgo_display(),
                    }
                    for h in historico_queryset
                ],
            }
        )


# 3. FILTRO HISTÓRICO
class HistoricoRiesgoFiltroView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo_iso):
        # Filtros existentes
        fecha_desde = request.query_params.get("desde")
        fecha_hasta = request.query_params.get("hasta")

        # NUEVO: Filtro por nivel de riesgo (Query Param: ?nivel=CRITICO)
        nivel_param = request.query_params.get("nivel")

        queryset = IndiceRiesgo.objects.filter(
            pais__codigo_iso=codigo_iso.upper()
        ).order_by(
            "-fecha_calculo"
        )  # Siempre ordenado para consistencia

        if fecha_desde:
            queryset = queryset.filter(fecha_calculo__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_calculo__date__lte=fecha_hasta)
        if nivel_param:
            queryset = queryset.filter(nivel_riesgo=nivel_param.upper())

        if not fecha_desde and not fecha_hasta:
            queryset = queryset[:30]

        data = [
            {
                "fecha": item.fecha_calculo.strftime("%Y-%m-%d"),
                "indice": item.indice_compuesto,
                "nivel": item.get_nivel_riesgo_display(),
                "detalle_scores": {
                    "eco": item.score_economico,
                    "cam": item.score_cambiario,
                    "est": item.score_estabilidad,
                },
            }
            for item in queryset
        ]

        return Response(
            {
                "pais": codigo_iso.upper(),
                "puntos_datos": len(data),
                "historico": data,
            }
        )


# 4. CÁLCULO MASIVO (SOLO ADMIN)
class CalcularRiesgoMasivoView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        paises = Pais.objects.all()
        registros_creados = 0
        try:
            with transaction.atomic():
                for pais in paises:
                    s_eco = round(random.uniform(10, 90), 2)
                    s_cam = round(random.uniform(10, 90), 2)
                    s_est = round(random.uniform(10, 90), 2)
                    idx = round((s_eco + s_cam + s_est) / 3, 2)

                    if idx < 30:
                        nivel = IndiceRiesgo.NivelRiesgo.BAJO
                    elif idx < 60:
                        nivel = IndiceRiesgo.NivelRiesgo.MODERADO
                    elif idx < 85:
                        nivel = IndiceRiesgo.NivelRiesgo.ALTO
                    else:
                        nivel = IndiceRiesgo.NivelRiesgo.CRITICO

                    IndiceRiesgo.objects.create(
                        pais=pais,
                        score_economico=s_eco,
                        score_cambiario=s_cam,
                        score_estabilidad=s_est,
                        indice_compuesto=idx,
                        nivel_riesgo=nivel,
                        detalle_calculo={
                            "motor": "V1.0",
                            "ejecutado_por": request.user.username,
                        },
                    )
                    registros_creados += 1
            return Response(
                {
                    "status": "success",
                    "mensaje": f"Completado para {registros_creados} países.",
                }
            )
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


# 5. DASHBOARD RESUMEN (CORREGIDO PARA SQLITE)
class DashboardResumenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # KPIs Básicos
        total_paises = Pais.objects.count()
        alertas_activas = Alerta.objects.filter(
            Q(usuario=request.user) | Q(usuario__isnull=True), leida=False
        ).count()
        total_portafolios = Portafolio.objects.filter(usuario=request.user).count()

        # Promedio de Riesgo Global (Lógica compatible con SQLite)
        ultimo_riesgo_promedio = 0
        ultimos_ids = (
            IndiceRiesgo.objects.values("pais")
            .annotate(ultimo_id=Max("id"))
            .values_list("ultimo_id", flat=True)
        )

        if ultimos_ids:
            ultimo_riesgo_promedio = IndiceRiesgo.objects.filter(
                id__in=ultimos_ids
            ).aggregate(Avg("indice_compuesto"))["indice_compuesto__avg"]

        return Response(
            {
                "kpis": {
                    "total_paises": total_paises,
                    "alertas_pendientes": alertas_activas,
                    "mis_portafolios": total_portafolios,
                    "promedio_riesgo_global": (
                        round(ultimo_riesgo_promedio, 2)
                        if ultimo_riesgo_promedio
                        else 0
                    ),
                },
                "usuario": request.user.username,
            }
        )


class DashboardMapaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Obtener los últimos IDs de riesgo de cada país
        ultimos_ids = (
            IndiceRiesgo.objects.values("pais")
            .annotate(ultimo_id=Max("id"))
            .values_list("ultimo_id", flat=True)
        )

        # 2. Obtener los datos completos de esos registros
        indices = (
            IndiceRiesgo.objects.filter(id__in=ultimos_ids)
            .select_related("pais")
            .only(
                "pais__nombre",
                "pais__codigo_iso",
                "pais__latitud",
                "pais__longitud",
                "indice_compuesto",
                "nivel_riesgo",
            )
        )

        # 3. Mapeo de colores según nivel
        colores_mapa = {
            "BAJO": "#22c55e",
            "MODERADO": "#eab308",
            "ALTO": "#f97316",
            "CRITICO": "#ef4444",
        }

        data = []
        for h in indices:
            # Asumimos que el modelo Pais tiene campos latitud y longitud
            data.append(
                {
                    "id": h.pais.pk,
                    "nombre": h.pais.nombre,
                    "codigo_iso": h.pais.codigo_iso,
                    "coordenadas": {"lat": h.pais.latitud, "lng": h.pais.longitud},
                    "indicadores": {
                        "indice": h.indice_compuesto,
                        "nivel": h.get_nivel_riesgo_display(),
                        "color": colores_mapa.get(
                            h.nivel_riesgo, "#94a3b8"
                        ),  # Gris si no hay match
                    },
                }
            )

        return Response(data)


class DashboardTendenciasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Definir el rango de tiempo (últimos 5 años)
        anio_actual = timezone.now().year
        anio_inicio = anio_actual - 4

        # 2. Agrupar y promediar por año
        tendencias = (
            IndiceRiesgo.objects.filter(fecha_calculo__year__gte=anio_inicio)
            .annotate(anio=ExtractYear("fecha_calculo"))
            .values("anio")
            .annotate(
                promedio_riesgo=Avg("indice_compuesto"),
                avg_economico=Avg("score_economico"),
                avg_cambiario=Avg("score_cambiario"),
                avg_estabilidad=Avg("score_estabilidad"),
            )
            .order_by("anio")
        )

        # 3. Formatear para gráficas de líneas
        labels = []
        data_riesgo = []
        data_detalle = {"economico": [], "cambiario": [], "estabilidad": []}

        for entry in tendencias:
            labels.append(str(entry["anio"]))
            data_riesgo.append(round(entry["promedio_riesgo"], 2))
            data_detalle["economico"].append(round(entry["avg_economico"], 2))
            data_detalle["cambiario"].append(round(entry["avg_cambiario"], 2))
            data_detalle["estabilidad"].append(round(entry["avg_estabilidad"], 2))

        return Response(
            {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Índice de Riesgo Global",
                        "data": data_riesgo,
                        "borderColor": "#3b82f6",
                    },
                    {
                        "label": "Score Económico",
                        "data": data_detalle["economico"],
                        "borderColor": "#10b981",
                    },
                ],
                "metadatos": {
                    "rango": f"{anio_inicio} - {anio_actual}",
                    "puntos": len(labels),
                },
            }
        )
