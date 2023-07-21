from django.urls import path

from .views import (
    RefbookListAPIView,
    RefbookElementListAPIView,
    RefbookElementCheckAPIView,
)

app_name = "refbooks"

urlpatterns = [
    path("refbooks/", RefbookListAPIView.as_view(), name="refbook_list"),
    path(
        "refbooks/<int:pk>/elements",
        RefbookElementListAPIView.as_view(),
        name="refbook_element_list",
    ),
    path(
        "refbooks/<int:pk>/check_element",
        RefbookElementCheckAPIView.as_view(),
        name="refbook_element_check",
    ),
]
