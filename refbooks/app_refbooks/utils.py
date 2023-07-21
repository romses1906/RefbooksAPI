from datetime import datetime

from django.utils import timezone

from .models import RefbookVersion


def get_current_version(refbook_id):
    """Функция для получения текущей версии справочника"""
    date_now = datetime.now(tz=timezone.utc)
    current_version = (
        RefbookVersion.objects.filter(refbook_id=refbook_id, start_date__lte=date_now)
        .order_by("start_date")
        .last()
    )
    return current_version
