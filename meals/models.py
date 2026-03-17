from django.core.validators import MinValueValidator
from django.db import models

from inventory.models import Product


class Dish(models.Model):
    """
    Модел за ястие с основните му хранителни стойности.
    Данните се използват при изчисляване на калории и макроси
    в дневното и седмичното меню.
    """

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

    products = models.ManyToManyField(
        Product,
        through="DishIngredient",
        related_name="dishes",
        blank=True,
        verbose_name="Продукти",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ястие"
        verbose_name_plural = "Ястия"

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    """
    Междинен модел между ястие и продукт.
    Пази кой продукт участва в ястието и в какво количество.
    """

    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Ястие",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="dish_ingredients",
        verbose_name="Продукт",
    )

    quantity = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        validators=[MinValueValidator(1)],
        verbose_name="Количество",
        help_text="Количеството от продукта, което се използва в ястието.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dish", "product"],
                name="unique_product_per_dish",
            )
        ]
        ordering = ("dish", "product__name")
        verbose_name = "Съставка на ястие"
        verbose_name_plural = "Съставки на ястия"

    def __str__(self):
        return (
            f"{self.dish.name} - "
            f"{self.product.full_name} "
            f"({self.quantity} {self.product.get_unit_short()})"
        )