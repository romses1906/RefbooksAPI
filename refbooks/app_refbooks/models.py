from django.db import models


class Refbook(models.Model):
    """Модель справочника"""

    code = models.CharField(max_length=100, verbose_name="код справочника", unique=True)
    name = models.CharField(max_length=300, verbose_name="наименование справочника")
    description = models.TextField(
        null=True, blank=True, verbose_name="описание справочника"
    )

    class Meta:
        verbose_name = "справочник"
        verbose_name_plural = "справочники"

    def __str__(self):
        return self.name


class RefbookVersion(models.Model):
    """Модель версии справочника"""

    refbook = models.ForeignKey(
        "Refbook",
        on_delete=models.CASCADE,
        related_name="refbook_versions",
        verbose_name="справочник",
    )
    version = models.CharField(max_length=50, verbose_name="версия справочника")
    start_date = models.DateField(verbose_name="дата начала действия версии")

    class Meta:
        verbose_name = "версия справочника"
        verbose_name_plural = "версии справочников"
        constraints = (
            models.UniqueConstraint(
                fields=["refbook", "version"], name="unique refbook version"
            ),
            models.UniqueConstraint(
                fields=["refbook", "start_date"],
                name="unique refbook version start_date",
            ),
        )

    def __str__(self):
        return f"{self.refbook.name}: {self.version}"


class RefbookElement(models.Model):
    """Модель элемента справочника"""

    refbook_version = models.ForeignKey(
        "RefbookVersion",
        on_delete=models.CASCADE,
        related_name="refbook_elements",
        verbose_name="версия справочника",
    )
    code = models.CharField(max_length=100, verbose_name="код элемента")
    value = models.CharField(max_length=300, verbose_name="значение элемента")

    class Meta:
        verbose_name = "элемент справочника"
        verbose_name_plural = "элементы справочников"
        constraints = (
            models.UniqueConstraint(
                fields=["refbook_version", "code"],
                name="unique element code of refbook version",
            ),
        )
