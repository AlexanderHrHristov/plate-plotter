from django.db import models
from django.core.validators import MinValueValidator


class Dish(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Ястие",
    )

    calories = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Калории",
    )

    protein = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Белтъчини",
    )

    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Въглехидрати",
    )

    fat = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Мазнини",
    )

    note = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Бележка",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ястие"
        verbose_name_plural = "Ястия"

    def __str__(self):
        return self.name