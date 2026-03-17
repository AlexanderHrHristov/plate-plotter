from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal



class Product(models.Model):
    """
    Основен модел за хранителните продукти в приложението. Съдържа:
    - име и марка
    - категория
    - мерна единица
    - хранителни стойности за 100 g
    """

    UNIT_GRAMS = "g"
    UNIT_PIECES = "pcs"

    UNIT_CHOICES = [
        (UNIT_GRAMS, "Грамове (g)"),
        (UNIT_PIECES, "Брой"),
    ]

    CATEGORY_MEAT_FISH = "meat_fish"
    CATEGORY_MILK_CHEESE = "milk_cheese"
    CATEGORY_GRAINS_LEGUMES = "grains_legumes"
    CATEGORY_FRUIT_VEGETABLES = "fruit_vegetables"
    CATEGORY_NUTS_OILS = "nuts_oils"
    CATEGORY_DESSERTS_SWEETS = "desserts_sweets"
    CATEGORY_DRINKS = "drinks"
    CATEGORY_PACKAGED_STORE = "packaged_store"
    CATEGORY_SPICES = "spices"

    CATEGORY_CHOICES = [
        (CATEGORY_MEAT_FISH, "Месо, риба, яйца"),
        (CATEGORY_MILK_CHEESE, "Млечни продукти"),
        (CATEGORY_GRAINS_LEGUMES, "Зърнени храни и бобови"),
        (CATEGORY_FRUIT_VEGETABLES, "Плодове и зеленчуци"),
        (CATEGORY_NUTS_OILS, "Ядки и мазнини"),
        (CATEGORY_DESSERTS_SWEETS, "Десерти и сладки"),
        (CATEGORY_DRINKS, "Напитки"),
        (CATEGORY_PACKAGED_STORE, "Готови храни"),
        (CATEGORY_SPICES, "Подправки")
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

    # Хранителните стойности са на база 100 g или мл.
    # от даден продукт.
    
    calories_per_100 = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Kcal / 100g",
    )
    protein_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Белтъчини / 100g",
    )
    carbs_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Въглехидрати / 100g",
    )
    fat_per_100 = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Мазнини / 100g",
    )

    is_basic = models.BooleanField(
        default=False,
        verbose_name="Базов продукт",
        help_text="Основен продукт- трябва да има наличност.",
    )

    class Meta:
        unique_together = ("name", "brand")
        ordering = ["name", "brand"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def clean(self):


        super().clean()

        if self.name:
            self.name = self.name.strip()

        if self.brand:
            self.brand = self.brand.strip()

        
        if self.brand == "":  # Ако остава празна марка със spaces.
            self.brand = ""

        nutrition_fields = [
            self.protein_per_100,
            self.carbs_per_100,
            self.fat_per_100,
        ]

        for value in nutrition_fields:
            if value is not None and value < 0:
                raise ValidationError("Хранителните стойности не могат да бъдат отрицателни.")

        if self.calories_per_100 < 0:
            raise ValidationError("Калориите не могат да бъдат отрицателни.")

    def save(self, *args, **kwargs):
       
        if self.name:
            self.name = self.name.strip()

        if self.brand:
            self.brand = self.brand.strip()

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """
        Показва име + марка, ако има марка.
        Ако не - само името.
        """
        if self.brand:
            return f"{self.name} {self.brand}"
        return self.name

    @property
    def macros(self):

        return {
            "protein": self.protein_per_100,
            "carbs": self.carbs_per_100,
            "fat": self.fat_per_100,
        }

    def get_unit_short(self):
        if self.unit == self.UNIT_GRAMS:
            return "g"
        return "бр."

    def __str__(self):
        return self.full_name



class Inventory(models.Model):
    """
    Наличност за конкретен продукт от който имаме наличен.
    към момента вкъщи.
    """

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="Продукт",
    )

    available_quantity = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Налично количество",
    )

    minimum_quantity = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Минимално количество",
        help_text="При падане под минимално - продукта влиза в списъка за пазаруване.",
    )


    class Meta:
        ordering = ["product__name"]
        verbose_name = "Наличност"
        verbose_name_plural = "Наличности"

    def clean(self):
        super().clean()

        if self.available_quantity < 0:
            raise ValidationError("Наличното количество не може да е отрицателно.")

        if self.minimum_quantity < 0:
            raise ValidationError("Минималното количество не може да е отрицателно.")

    @property
    def is_below_minimum(self):
        return self.available_quantity < self.minimum_quantity


    @property
    def shortage_amount(self):
        """
        Колко не достига до минималната наличност.
        Ако всичко е наред, трябва да връща 0.
        """
        if self.is_below_minimum:
            return self.minimum_quantity - self.available_quantity
        return Decimal("0")

    def needs_restock(self):

        return self.is_below_minimum


    def get_status_label(self):
        if self.available_quantity == 0:
            return "Изчерпан"
        if self.is_below_minimum:
            return "Под минимум"
        return "Наличен"

    def __str__(self):
        return f"{self.product.full_name} - {self.available_quantity} {self.product.get_unit_short()}"