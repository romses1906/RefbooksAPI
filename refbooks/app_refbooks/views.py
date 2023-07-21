from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Refbook, RefbookElement
from .serializers import RefbookListSerializer, ElementListSerializer
from .utils import get_current_version


@extend_schema(
    summary="Получение списка справочников",
    parameters=[
        OpenApiParameter(
            name="date",
            location=OpenApiParameter.QUERY,
            description="constraint date",
            required=False,
        ),
    ],
)
class RefbookListAPIView(APIView):
    """Представление для получения списка справочников"""

    def get(self, request):
        queryset = Refbook.objects.all()
        date = request.query_params.get("date")
        if date:
            queryset = queryset.filter(
                refbook_versions__start_date__lte=date
            ).distinct()
        return Response(RefbookListSerializer({"refbooks": queryset}).data)


@extend_schema(
    summary="Получение списка элементов версии справочника",
    parameters=[
        OpenApiParameter(
            name="version",
            location=OpenApiParameter.QUERY,
            description="concrete version",
            required=False,
        ),
    ],
)
class RefbookElementListAPIView(APIView):
    """Представление для получения списка элементов версии справочника"""

    def get(self, request, pk):
        version_title = request.query_params.get("version")
        if not version_title:
            version_title = get_current_version(refbook_id=pk).version
        queryset = RefbookElement.objects.filter(
            refbook_version__refbook_id=pk, refbook_version__version=version_title
        )
        return Response(ElementListSerializer({"elements": queryset}).data)


@extend_schema(
    summary="Валидация элемента версии справочника",
    parameters=[
        OpenApiParameter(
            name="code",
            location=OpenApiParameter.QUERY,
            description="element code",
            required=True,
        ),
        OpenApiParameter(
            name="value",
            location=OpenApiParameter.QUERY,
            description="element value",
            required=True,
        ),
        OpenApiParameter(
            name="version",
            location=OpenApiParameter.QUERY,
            description="element version",
            required=False,
        ),
    ],
)
class RefbookElementCheckAPIView(APIView):
    """Представление для валидации элемента версии справочника"""

    def get(self, request, pk):
        element_code = request.query_params.get("code")
        element_value = request.query_params.get("value")
        version_title = request.query_params.get("version")
        if not version_title:
            version_title = get_current_version(refbook_id=pk).version
        check_element = RefbookElement.objects.filter(
            refbook_version__version=version_title,
            code=element_code,
            value=element_value,
        )
        if check_element:
            return Response({"result": True})
        return Response({"result": False})
