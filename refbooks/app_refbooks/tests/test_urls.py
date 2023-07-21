from app_refbooks.models import Refbook
from app_refbooks.views import (
    RefbookListAPIView,
    RefbookElementListAPIView,
    RefbookElementCheckAPIView,
)
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase


class RefbookListPageTest(APITestCase):
    """Тестирование URL списка справочников"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse("refbooks:refbook_list")
        cls.response = cls.client.get(cls.url)

    def test_page_uses_the_correct_url(self):
        """Тестирование используемого URL"""
        self.assertURLEqual(self.url, "/refbooks/")

    def test_url_uses_the_desired_view(self):
        """Тестирование использования ожидаемого представления по данному URL"""
        view = resolve(self.url)
        desired_view = RefbookListAPIView.as_view().__name__
        self.assertEqual(view.func.__name__, desired_view)


class RefbookElementListPageTest(APITestCase):
    """Тестирование URL списка элементов версии справочника"""

    fixtures = [
        "005_refbooks.json",
        "010_refbook_versions.json",
        "015_refbook_elements.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.refbook = Refbook.objects.first()
        cls.client = APIClient()
        cls.url = reverse(
            "refbooks:refbook_element_list", kwargs={"pk": cls.refbook.pk}
        )
        cls.response = cls.client.get(cls.url)

    def test_page_uses_the_correct_url(self):
        """Тестирование используемого URL"""
        refbook_pk = self.refbook.pk
        self.assertURLEqual(self.url, f"/refbooks/{refbook_pk}/elements")

    def test_url_uses_the_desired_view(self):
        """Тестирование использования ожидаемого представления по данному URL"""
        view = resolve(self.url)
        desired_view = RefbookElementListAPIView.as_view().__name__
        self.assertEqual(view.func.__name__, desired_view)


class RefbookElementCheckPageTest(APITestCase):
    """Тестирование URL валидации элемента справочника"""

    fixtures = [
        "005_refbooks.json",
        "010_refbook_versions.json",
        "015_refbook_elements.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.refbook = Refbook.objects.first()
        cls.client = APIClient()
        cls.url = reverse(
            "refbooks:refbook_element_check", kwargs={"pk": cls.refbook.pk}
        )
        cls.response = cls.client.get(cls.url)

    def test_page_uses_the_correct_url(self):
        """Тестирование используемого URL"""
        refbook_pk = self.refbook.pk
        self.assertURLEqual(self.url, f"/refbooks/{refbook_pk}/check_element")

    def test_url_uses_the_desired_view(self):
        """Тестирование использования ожидаемого представления по данному URL"""
        view = resolve(self.url)
        desired_view = RefbookElementCheckAPIView.as_view().__name__
        self.assertEqual(view.func.__name__, desired_view)
