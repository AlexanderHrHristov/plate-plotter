from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from inventory.models import Product
from meals.models import Dish


class WeekMenuModel(models.Model):
    """
    Представя седмично меню, започващо от определена дата.
    Към него са свързани отделните хранения за всеки ден.
    """

    start_date = models.DateField(
        unique=True,
        verbose_name="Начален ден на седмицата",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Бележки",
    )

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Седмично меню"
        verbose_name_plural = "Седмични менюта"

    def __str__(self):
        return f"Седмица от {self.start_date}"

    def entries_for_day(self, day):
        """Връща всички записи за конкретен ден."""
        return self.meals.filter(day=day)

    def total_calories_for_day(self, day):
        total = sum(meal.total_calories() for meal in self.meals.filter(day=day))
        return round(total, 2)

    def total_protein_for_day(self, day):
        total = sum(meal.total_protein() for meal in self.meals.filter(day=day))
        return round(total, 2)

    def total_carbs_for_day(self, day):
        total = sum(meal.total_carbs() for meal in self.meals.filter(day=day))
        return round(total, 2)

    def total_fat_for_day(self, day):
        total = sum(meal.total_fat() for meal in self.meals.filter(day=day))
        return round(total, 2)

    def total_calories_for_week(self):
        total = sum(meal.total_calories() for meal in self.meals.all())
        return round(total, 2)

    def total_protein_for_week(self):
        total = sum(meal.total_protein() for meal in self.meals.all())
        return round(total, 2)

    def total_carbs_for_week(self):
        total = sum(meal.total_carbs() for meal in self.meals.all())
        return round(total, 2)

    def total_fat_for_week(self):
        total = sum(meal.total_fat() for meal in self.meals.all())
        return round(total, 2)


class Meal(models.Model):
    """
    Един запис в седмичното меню.
    Представя конкретно хранене за даден ден,
    което може да бъде или ястие, или отделен продукт.
    """

    DAY_CHOICES = [
        (1, "Понеделник"),
        (2, "Вторник"),
        (3, "Сряда"),
        (4, "Четвъртък"),
        (5, "Петък"),
        (6, "Събота"),
        (7, "Неделя"),
    ]

    week_menu = models.ForeignKey(
        WeekMenuModel,
        on_delete=models.CASCADE,
        related_name="meals",
    )

    day = models.IntegerField(
        choices=DAY_CHOICES,
        verbose_name="Ден",
    )

    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ястие",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Продукт",
    )

    quantity = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        default=100,
        validators=[MinValueValidator(1)],
        verbose_name="Количество",
        help_text="За продукт – грамове или брой. За ястие обикновено остава 1.",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Бележки",
    )

    class Meta:
        ordering = ("day", "id")
        verbose_name = "Запис в меню"
        verbose_name_plural = "Записи в меню"

    def __str__(self):
        item_name = self.dish or self.product or "Без избор"
        return f"{self.week_menu} - {self.get_day_display()} - {item_name}"

    def clean(self):
        """Гарантира, че е избрано или ястие, или продукт."""
        if not self.dish and not self.product:
            raise ValidationError("Избери ястие или продукт.")

        if self.dish and self.product:
            raise ValidationError(
                "Може да избереш само едно от двете: ястие или продукт."
            )

    def total_calories(self):
        if self.dish:
            return Decimal(self.dish.calories)

        if self.product:
            return round(
                (self.quantity / Decimal("100"))
                * Decimal(self.product.calories_per_100),
                2,
            )

        return Decimal("0")

    def total_protein(self):
        if self.dish:
            return Decimal(self.dish.protein)

        if self.product:
            return round(
                (self.quantity / Decimal("100"))
                * Decimal(self.product.protein_per_100),
                2,
            )

        return Decimal("0")

    def total_carbs(self):
        if self.dish:
            return Decimal(self.dish.carbs)

        if self.product:
            return round(
                (self.quantity / Decimal("100"))
                * Decimal(self.product.carbs_per_100),
                2,
            )

        return Decimal("0")

    def total_fat(self):
        if self.dish:
            return Decimal(self.dish.fat)

        if self.product:
            return round(
                (self.quantity / Decimal("100"))
                * Decimal(self.product.fat_per_100),
                2,
            )

        return Decimal("0")