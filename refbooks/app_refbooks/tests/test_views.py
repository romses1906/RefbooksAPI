import json
from datetime import datetime

from app_refbooks.models import Refbook, RefbookVersion, RefbookElement
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase


class RefbookListAPIViewTest(APITestCase):
    """Тестирование представления для отображения списка справочников"""

    fixtures = [
        "005_refbooks.json",
        "010_refbook_versions.json",
        "015_refbook_elements.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.refbooks = Refbook.objects.all()
        self.url = reverse("refbooks:refbook_list")
        self.response = self.client.get(self.url)

    def test_view_returns_correct_http_status(self):
        """Тестирование возврата корректного http-кода при открытии страницы справочников"""
        self.assertEqual(self.response.status_code, 200)

    def test_refbooks_count_is_correct(self):
        """Тестирование количества выводимых справочников"""
        self.assertTrue(len(self.response.data["refbooks"]) == self.refbooks.count())

    def test_refbooks_response_is_correct(self):
        """Тестирование корректности ответа при запросе всех справочников"""
        self.assertEqual(
            self.response.data,
            {
                "refbooks": [
                    {"id": 1, "code": "MS1", "name": "Справочник MS1"},
                    {"id": 2, "code": "ICD-10", "name": "Справочник ICD-10"},
                ]
            },
        )

    def test_refbooks_with_date_is_correct(self):
        """Тестирование выводимых справочников при запросе c ограничением даты начала действия версии"""
        test_date = "2022-12-12"
        url_with_date = self.url + f"?date={test_date}"
        response_with_date = self.client.get(url_with_date)
        self.assertTrue(len(response_with_date.data["refbooks"]) == 1)
        self.assertEqual(
            json.loads(response_with_date.content),
            {"refbooks": [{"id": 1, "code": "MS1", "name": "Справочник MS1"}]},
        )


class RefbookElementListAPIViewTest(APITestCase):
    """Тестирование представления для отображения элементов версии справочника"""

    fixtures = [
        "005_refbooks.json",
        "010_refbook_versions.json",
        "015_refbook_elements.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.date_now = datetime.now(tz=timezone.utc)
        self.refbook = Refbook.objects.first()
        self.url = reverse(
            "refbooks:refbook_element_list", kwargs={"pk": self.refbook.pk}
        )
        self.response = self.client.get(self.url)

    def test_view_returns_correct_http_status(self):
        """Тестирование возврата корректного http-кода при открытии страницы элементов версии справочников"""
        self.assertEqual(self.response.status_code, 200)

    def test_refbook_elements_count_is_correct(self):
        """Тестирование количества выводимых элементов текущей версии справочника"""
        current_version = (
            RefbookVersion.objects.filter(
                refbook_id=self.refbook.pk, start_date__lte=self.date_now
            )
            .order_by("start_date")
            .last()
        )
        desired_elements = RefbookElement.objects.filter(
            refbook_version=current_version
        )
        self.assertTrue(len(self.response.data["elements"]) == desired_elements.count())

    def test_refbook_elements_of_concrete_version_is_correct(self):
        """Тестирование выводимых элементов конкретно заданной версии справочника"""
        url_with_version = self.url + "?version=1.0"
        response_with_version = self.client.get(url_with_version)
        self.assertTrue(len(response_with_version.data["elements"]) == 2)
        self.assertEqual(
            json.loads(response_with_version.content),
            {
                "elements": [
                    {"code": "J00", "value": "test_value J00"},
                    {"code": "J01", "value": "test_value J01"},
                ]
            },
        )


class RefbookElementCheckAPIViewTest(APITestCase):
    """Тестирование представления для валидации элемента версии справочника"""

    fixtures = [
        "005_refbooks.json",
        "010_refbook_versions.json",
        "015_refbook_elements.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.exists_code = "C002"
        self.exists_value = "test_value C002"
        self.refbook = Refbook.objects.first()
        self.url = (
                reverse("refbooks:refbook_element_check", kwargs={"pk": self.refbook.pk})
                + f"?code={self.exists_code}&value={self.exists_value}"
        )
        self.response = self.client.get(self.url)

    def test_view_returns_correct_http_status(self):
        """Тестирование возврата корректного http-кода при открытии страницы валидации элемента версии справочника"""
        self.assertEqual(self.response.status_code, 200)

    def test_validate_refbook_element_in_current_version_is_correct(self):
        """Тестирование валидации элемента справочника в текущей версии справочника"""
        self.assertEqual(json.loads(self.response.content), {"result": True})

    def test_validate_refbook_element_of_concrete_version_is_correct(self):
        """Тестирование валидации элемента справочника в конкретно заданной версии справочника"""
        url_with_version = self.url + f"&version=1.0"
        response_with_version = self.client.get(url_with_version)
        self.assertEqual(json.loads(response_with_version.content), {"result": False})
