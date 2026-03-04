import io
from django.db.models import Q, Sum, Count
from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, filters  # <--- Agregado filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django_filters.rest_framework import (
    DjangoFilterBackend,
)  # <--- Agregado DjangoFilter

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import Portafolio
from .serializers import PortafolioSerializer, PortafolioDetalleSerializer
from position.models import Posicion

from core.pagination import StandardResultsSetPagination
from rest_framework import generics, filters, permissions
from core.permissions import IsAnalistaRole


class PortafolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortafolioSerializer
    pagination_class = StandardResultsSetPagination

    # --- REQUISITOS TRANSVERSALES: FILTROS, BÚSQUEDA Y ORDEN ---
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["es_publico"]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "fecha_creacion"]
    ordering = ["nombre"]

    # --- REQUISITO TRANSVERSAL: PERMISOS POR ROL ---
    def get_permissions(self):
        """
        Asigna permisos dinámicamente según el método HTTP.
        """
        if self.request.method == "POST":
            # Solo ADMIN y ANALISTA pueden crear portafolios
            return [IsAnalistaRole()]

        # Para el método GET (Listar), cualquier usuario autenticado (incluye VIEWER)
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Tu lógica de seguridad de datos existente se mantiene...
        user = self.request.user
        return Portafolio.objects.filter(
            (Q(usuario=user) | Q(es_publico=True)), activo=True
        ).distinct()

    def get_queryset(self):
        user = self.request.user
        return Portafolio.objects.filter(
            (Q(usuario=user) | Q(es_publico=True)), activo=True
        ).distinct()

    def perform_create(self, serializer):
        try:
            serializer.save(usuario=self.request.user)
        except ValidationError as e:
            raise DRFValidationError(e.message_dict)


# CAMBIO AQUÍ: Heredamos de RetrieveUpdateDestroyAPIView
class PortafolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Si el usuario va a editar (PUT/PATCH), usamos el serializer básico.
        # Si solo va a ver (GET), usamos el de detalle con métricas.
        if self.request.method in ["PUT", "PATCH"]:
            return PortafolioSerializer
        return PortafolioDetalleSerializer

    def get_queryset(self):
        user = self.request.user

        # LÓGICA DE SEGURIDAD:
        # Si es una acción de escritura (PUT, PATCH, DELETE): Solo mis portafolios.
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return Portafolio.objects.filter(usuario=user, activo=True)

        # Si es lectura (GET): Mis portafolios O los públicos.
        return Portafolio.objects.filter(
            Q(usuario=user) | Q(es_publico=True), activo=True
        )

    def perform_update(self, serializer):
        try:
            # Al actualizar, el modelo ejecutará full_clean() y validará si es VIEWER
            serializer.save()
        except ValidationError as e:
            raise DRFValidationError(e.message_dict)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescribimos para devolver un mensaje personalizado
        en lugar de solo el 204 estándar.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"El portafolio '{instance.nombre}' ha sido eliminado correctamente."
            },
            status=status.HTTP_200_OK,  # O HTTP_204_NO_CONTENT si prefieres el estándar
        )

    def perform_destroy(self, instance):
        """
        Esta es la clave del Soft Delete:
        No borramos el objeto, solo cambiamos su estado.
        """
        instance.activo = False
        instance.save()


class PortafolioResumenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 1. Validar que el portafolio exista y pertenezca al usuario
        portafolio = generics.get_object_or_404(Portafolio, pk=pk, usuario=request.user)

        # 2. Obtener solo las posiciones activas (sin fecha_salida)
        posiciones = Posicion.objects.filter(
            portafolio=portafolio, fecha_salida__isnull=True
        )

        # 3. Calcular distribución por país
        por_pais = posiciones.values("pais").annotate(total=Sum("monto_inversion_usd"))

        # 4. Calcular distribución por tipo de activo
        por_tipo = posiciones.values("tipo_activo").annotate(
            total=Sum("monto_inversion_usd")
        )

        # 5. Calcular total general
        total_gen = (
            posiciones.aggregate(Sum("monto_inversion_usd"))["monto_inversion_usd__sum"]
            or 0
        )

        return Response(
            {
                "portafolio": portafolio.nombre,
                "total_invertido_usd": total_gen,
                "distribucion_pais": {item["pais"]: item["total"] for item in por_pais},
                "distribucion_tipo_activo": {
                    item["tipo_activo"]: item["total"] for item in por_tipo
                },
            }
        )


class ExportarPortafolioPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 1. Obtener datos
        portafolio = get_object_or_404(Portafolio, pk=pk, usuario=request.user)
        posiciones = Posicion.objects.filter(portafolio=portafolio)

        # 2. Crear un buffer en memoria para el PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # 3. Diseño del PDF: Título
        elements.append(
            Paragraph(f"Reporte de Portafolio: {portafolio.nombre}", styles["Title"])
        )
        elements.append(Paragraph(f"Fecha: 2026-03-04", styles["Normal"]))
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))

        # 4. Tabla de Posiciones
        data = [
            ["Tipo de Activo", "País", "Monto (USD)", "Fecha Entrada"]
        ]  # Encabezados corregidos
        for pos in posiciones:
            data.append(
                [
                    pos.get_tipo_activo_display(),  # Muestra "Renta Fija" en vez de "RENTA_FIJA"
                    str(pos.pais),  # Usa el __str__ del modelo Pais
                    f"${pos.monto_inversion_usd}",
                    pos.fecha_entrada.strftime("%d/%m/%Y"),  # Formato de fecha bonito
                ]
            )

        # Estilo de la tabla
        tabla = Table(data)
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.lightgrey],
                ),
            ]
        )
        tabla.setStyle(style)
        elements.append(tabla)

        # 5. Construir PDF
        doc.build(elements)
        buffer.seek(0)

        # 6. Devolver respuesta de archivo
        return FileResponse(
            buffer, as_attachment=True, filename=f"Reporte_{portafolio.id}.pdf"
        )
