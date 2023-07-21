from app_refbooks.models import Refbook, RefbookVersion, RefbookElement
from django.db.backends.sqlite3.base import IntegrityError
from rest_framework.test import APITestCase


class RefbookModelTest(APITestCase):
    """Класс тестов модели Справочник"""

    @classmethod
    def setUpTestData(cls):
        cls.refbook = Refbook.objects.create(code="test code", name="test name")

    def test_verbose_name(self):
        """Тестирование verbose_name полей модели Справочник"""
        refbook = self.refbook
        field_verboses = {
            "code": "код справочника",
            "name": "наименование справочника",
            "description": "описание справочника",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    refbook._meta.get_field(field).verbose_name, expected_value
                )

    def test_name_max_length(self):
        """Тестирование максимально возможной длины для ввода поля name модели Справочник"""
        refbook = self.refbook
        max_length = refbook._meta.get_field("name").max_length
        self.assertEqual(max_length, 300)

    def test_code_max_length(self):
        """Тестирование максимально возможной длины для ввода поля code модели Справочник"""
        refbook = self.refbook
        max_length = refbook._meta.get_field("code").max_length
        self.assertEqual(max_length, 100)

    def test_blank_fields(self):
        """Тестирование свойства blank полей модели Справочник"""
        refbook = self.refbook
        blank_fields = [
            "description",
        ]
        for field in blank_fields:
            with self.subTest(field=field):
                self.assertTrue(refbook._meta.get_field(field_name=field).blank)

    def test_null_fields(self):
        """Тестирование свойства null полей модели Справочник"""
        refbook = self.refbook
        null_fields = [
            "description",
        ]
        for field in null_fields:
            with self.subTest(field=field):
                self.assertTrue(refbook._meta.get_field(field_name=field).null)

    def test_unique_fields(self):
        """Тестирование уникальности поля code модели Справочник"""
        refbook = self.refbook
        unique_fields = [
            "code",
        ]
        for field in unique_fields:
            with self.subTest(field=field):
                self.assertTrue(refbook._meta.get_field(field_name=field).unique)


class RefbookVersionModelTest(APITestCase):
    """Класс тестов модели Версия справочника"""

    @classmethod
    def setUpTestData(cls):
        cls.refbook = Refbook.objects.create(code="test code", name="test name")
        cls.refbook_version = RefbookVersion.objects.create(
            refbook=cls.refbook, version="test 1.0", start_date="2023-01-01"
        )

    def test_verbose_name(self):
        """Тестирование verbose_name полей модели Версия справочника"""
        refbook_version = self.refbook_version
        field_verboses = {
            "refbook": "справочник",
            "version": "версия справочника",
            "start_date": "дата начала действия версии",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    refbook_version._meta.get_field(field).verbose_name, expected_value
                )

    def test_version_max_length(self):
        """Тестирование максимально возможной длины для ввода поля version модели Версия справочника"""
        refbook_version = self.refbook_version
        max_length = refbook_version._meta.get_field("version").max_length
        self.assertEqual(max_length, 50)

    def test_unique_version_of_refbook(self):
        """
        Тестирование ограничения создания версии справочника с названием версии, которое уже присутствует в БД
        """
        with self.assertRaises(Exception) as raised:
            RefbookVersion.objects.create(
                refbook=self.refbook, version="test 1.0", start_date="2023-01-05"
            )
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_unique_start_date_of_version_of_refbook(self):
        """
        Тестирование ограничения создания версии справочника с датой начала действия, которая уже присутствует в БД
        """
        with self.assertRaises(Exception) as raised:
            RefbookVersion.objects.create(
                refbook=self.refbook, version="test 2.0", start_date="2023-01-01"
            )
        self.assertEqual(IntegrityError, type(raised.exception))


class RefbookElementModelTest(APITestCase):
    """Класс тестов модели Элемент справочника"""

    @classmethod
    def setUpTestData(cls):
        cls.refbook = Refbook.objects.create(code="test code", name="test name")
        cls.refbook_version = RefbookVersion.objects.create(
            refbook=cls.refbook, version="test 1.0", start_date="2023-01-01"
        )
        cls.element = RefbookElement.objects.create(
            refbook_version=cls.refbook_version, code="test_code", value="test_value"
        )

    def test_verbose_name(self):
        """Тестирование verbose_name полей модели Элемент справочника"""
        element = self.element
        field_verboses = {
            "refbook_version": "версия справочника",
            "code": "код элемента",
            "value": "значение элемента",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    element._meta.get_field(field).verbose_name, expected_value
                )

    def test_code_max_length(self):
        """Тестирование максимально возможной длины для ввода поля code модели Элемент справочника"""
        element = self.element
        max_length = element._meta.get_field("code").max_length
        self.assertEqual(max_length, 100)

    def test_value_max_length(self):
        """Тестирование максимально возможной длины для ввода поля value модели Элемент справочника"""
        element = self.element
        max_length = element._meta.get_field("value").max_length
        self.assertEqual(max_length, 300)

    def test_unique_code_of_version(self):
        """
        Тестирование ограничения создания элемента справочника с кодом, который уже присутствует в БД
        """
        with self.assertRaises(Exception) as raised:
            RefbookElement.objects.create(
                refbook_version=self.refbook_version,
                code="test_code",
                value="test_value_2",
            )
        self.assertEqual(IntegrityError, type(raised.exception))
