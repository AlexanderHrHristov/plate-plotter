from django.db import models
from django.core.validators import MinValueValidator


class Store(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Магазин",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("g", "Грамове (g)"),
        ("pcs", "Опаковка (бр.)"),
    ]

    CATEGORY_CHOICES = [
        ("meat_fish", "Месо, риба, яйца"),
        ("milk_cheese", "Млечни продукти"),
        ("grains_legumes", "Зърнени храни и бобови"),
        ("fruit_vegetables", "Плодове и зеленчуци"),
        ("nuts_oils", "Ядки и мазнини"),
        ("desserts_sweets", "Десерти и сладки храни"),
        ("drinks", "Напитки"),
        ("packaged_store", "Готови храни"),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="Продукт",
    )

    brand = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Марка",
    )

    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Магазин",
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория",
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        verbose_name="Мерна единица",
    )

    calories_per_100 = models.PositiveIntegerField(
        default=0,
        verbose_name="Калории / 100g",
    )

    protein_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Белтъчини / 100g",
    )

    carbs_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Въглехидрати / 100g",
    )

    fat_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Мазнини / 100g",
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
        help_text="Цена за килограм или опаковка",
    )

    is_basic = models.BooleanField(
        default=False,
        verbose_name="Основен продукт",
        help_text="Продукт, от който винаги трябва да има наличност.",
    )

    class Meta:
        unique_together = ("name", "brand")

    def full_name(self):
        return f"{self.name} {self.brand}".strip()

    def __str__(self):
        return self.full_name()


class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="Продукт",
    )
    available_quantity = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Налично количество",
    )
    minimum_quantity = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Минимално количество",
    )

    @property
    def is_below_minimum(self):
        return self.available_quantity < self.minimum_quantity

    def __str__(self):
        unit_label = "g" if self.product.unit == "g" else "бр."
        return f"{self.product} - {self.available_quantity} {unit_label}"