from rest_framework import serializers

from .models import Refbook, RefbookElement


class RefbookSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Справочник"""

    class Meta:
        model = Refbook
        fields = [
            "id",
            "code",
            "name",
        ]


class RefbookElementSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Элемент справочника"""

    class Meta:
        model = RefbookElement
        fields = [
            "code",
            "value",
        ]


class RefbookListSerializer(serializers.Serializer):
    """Сериалайзер для вывода списка справочников"""

    refbooks = RefbookSerializer(many=True)


class ElementListSerializer(serializers.Serializer):
    """Сериалайзер для вывода элементов версии справочника"""

    elements = RefbookElementSerializer(many=True)
