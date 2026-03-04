from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import IndiceRiesgo
from rest_framework.permissions import IsAdminUser  # Solo administradores
import random  # Simulación de motor de cálculo
from countries.models import Pais
from django.utils import timezone
from django.db import transaction # Para asegurar que todo se guarde o nada


# 1. CLASE PARA EL RANKING GENERAL
class RankingRiesgoPaisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        indices = IndiceRiesgo.objects.select_related("pais").order_by(
            "-indice_compuesto"
        )
        data = []
        for item in indices:
            data.append(
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
            )
        return Response(data)


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
        data = {
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
        return Response(data)


class HistoricoRiesgoFiltroView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo_iso):
        # 1. Capturar fechas de los parámetros de la URL (?desde=YYYY-MM-DD&hasta=...)
        fecha_desde = request.query_params.get("desde")
        fecha_hasta = request.query_params.get("hasta")

        # 2. Base de la consulta
        queryset = IndiceRiesgo.objects.filter(
            pais__codigo_iso=codigo_iso.upper()
        ).order_by(
            "fecha_calculo"
        )  # Orden cronológico para gráficas

        # 3. Aplicar filtros si existen
        if fecha_desde:
            queryset = queryset.filter(fecha_calculo__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_calculo__date__lte=fecha_hasta)

        # Si no hay filtros, limitamos a los últimos 30 registros por defecto
        if not fecha_desde and not fecha_hasta:
            queryset = queryset[:30]

        # 4. Formatear respuesta
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
                "rango": {
                    "desde": fecha_desde or "inicio",
                    "hasta": fecha_hasta or "actualidad",
                },
                "puntos_datos": len(data),
                "historico": data,
            }
        )


class CalcularRiesgoMasivoView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        paises = Pais.objects.all()
        registros_creados = 0

        # Usamos transaction.atomic para que si falla un cálculo,
        # no queden datos a medias en la BD.
        try:
            with transaction.atomic():
                for pais in paises:
                    score_eco = round(random.uniform(10, 90), 2)
                    score_cam = round(random.uniform(10, 90), 2)
                    score_est = round(random.uniform(10, 90), 2)

                    indice_compuesto = round((score_eco + score_cam + score_est) / 3, 2)

                    # Lógica de niveles (Asegúrate de que coincidan con tus TextChoices)
                    if indice_compuesto < 30:
                        nivel = IndiceRiesgo.NivelRiesgo.BAJO
                    elif indice_compuesto < 60:
                        nivel = IndiceRiesgo.NivelRiesgo.MODERADO
                    elif indice_compuesto < 85:
                        nivel = IndiceRiesgo.NivelRiesgo.ALTO
                    else:
                        nivel = IndiceRiesgo.NivelRiesgo.CRITICO

                    IndiceRiesgo.objects.create(
                        pais=pais,
                        score_economico=score_eco,
                        score_cambiario=score_cam,
                        score_estabilidad=score_est,
                        indice_compuesto=indice_compuesto,
                        nivel_riesgo=nivel,
                        detalle_calculo={
                            "motor": "V1.0",
                            "ejecutado_por": request.user.username,
                        },
                    )
                    registros_creados += 1

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)

        return Response(
            {
                "status": "success",
                "mensaje": f"Recálculo completado para {registros_creados} países.",
                "fecha_ejecucion": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
