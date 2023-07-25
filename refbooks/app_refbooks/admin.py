from django.contrib import admin

from .models import Refbook, RefbookVersion, RefbookElement
from .utils import get_current_version


class RefbookTabularInline(admin.TabularInline):
    """Используется для отображения кода и наименования справочника в списке версий справочников в Django Admin"""

    model = Refbook
    fields = (
        "code",
        "name",
    )


class RefbookVersionInline(admin.StackedInline):
    """
    Используется для возможности редактирования имеющихся версий данного
    справочника при редактировании справочника в Django Admin
    """

    model = RefbookVersion


class RefbookElementInline(admin.StackedInline):
    """
    Используется для возможности редактирования элементов справочника
    данной версии при редактировании версии справочника в Django Admin
    """

    model = RefbookElement


class RefbookAdmin(admin.ModelAdmin):
    """
    Используется для настройки отображения и поведения модели справочников в Django Admin
    """

    list_display = (
        "id",
        "code",
        "name",
        "current_version",
        "date_current_version",
    )
    inlines = (RefbookVersionInline,)

    def date_current_version(self, obj):
        """Метод получения даты начала действия текущей версии справочника"""
        current_version = get_current_version(refbook_id=obj)
        if current_version:
            return current_version.start_date
        return '-'

    def current_version(self, obj):
        """Метод получения текущей версии справочника"""
        current_version = get_current_version(refbook_id=obj)
        if current_version:
            return current_version
        return '-'

    date_current_version.short_description = "Дата начала действия версии"
    current_version.short_description = "Текущая версия"


class RefbookVersionAdmin(admin.ModelAdmin):
    """
    Используется для настройки отображения и поведения модели версий справочников в Django Admin
    """

    list_display = (
        "refbook_code",
        "refbook_name",
        "version",
        "start_date",
    )
    inlines = (RefbookElementInline,)
    list_display_links = ("version",)

    def refbook_code(self, obj):
        """Метод получения кода справочника"""
        return obj.refbook.code

    def refbook_name(self, obj):
        """Метод получения наименования справочника"""
        return obj.refbook.name

    refbook_code.short_description = "Код справочника"
    refbook_name.short_description = "Наименование справочника"


class RefbookElementAdmin(admin.ModelAdmin):
    """
    Используется для настройки отображения и поведения модели элементов справочников в Django Admin
    """

    list_display = (
        "refbook_version",
        "code",
        "value",
    )


admin.site.register(Refbook, RefbookAdmin)
admin.site.register(RefbookVersion, RefbookVersionAdmin)
admin.site.register(RefbookElement, RefbookElementAdmin)
