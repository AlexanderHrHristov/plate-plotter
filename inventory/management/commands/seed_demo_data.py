from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from inventory.models import Product, Inventory
from meals.models import Dish
from weekmenu.models import WeekMenu, Meal

"""
Напълва ми базата данни с продукти, ястия и меню.
Скрипта се стартира с 

python manage.py seed_demo_data --reset

"""

class Command(BaseCommand):
    help = "Попълва базата с demo данни: продукти, наличности, ястия и седмично меню."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Изтрива старите данни и създава demo данните наново.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(self.style.WARNING("Изтривам старите данни..."))
            Meal.objects.all().delete()
            WeekMenu.objects.all().delete()
            Dish.objects.all().delete()
            Inventory.objects.all().delete()
            Product.objects.all().delete()

        self.stdout.write("Създавам demo продукти и наличности...")

        products_data = [
            {
                "name": "Пилешко филе",
                "brand": "",
                "category": Product.CATEGORY_MEAT_FISH,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 120,
                "protein_per_100": Decimal("23.0"),
                "carbs_per_100": Decimal("0.0"),
                "fat_per_100": Decimal("2.0"),
                "is_basic": True,
                "available_quantity": 400,
                "minimum_quantity": 500,
            },
            {
                "name": "Яйца",
                "brand": "",
                "category": Product.CATEGORY_MEAT_FISH,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 155,
                "protein_per_100": Decimal("13.0"),
                "carbs_per_100": Decimal("1.1"),
                "fat_per_100": Decimal("11.0"),
                "is_basic": True,
                "available_quantity": 4,
                "minimum_quantity": 10,
            },
            {
                "name": "Сьомга",
                "brand": "",
                "category": Product.CATEGORY_MEAT_FISH,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 208,
                "protein_per_100": Decimal("20.0"),
                "carbs_per_100": Decimal("0.0"),
                "fat_per_100": Decimal("13.0"),
                "is_basic": False,
                "available_quantity": 200,
                "minimum_quantity": 200,
            },
            {
                "name": "Кисело мляко",
                "brand": "Бор Чвор",
                "category": Product.CATEGORY_MILK_CHEESE,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 61,
                "protein_per_100": Decimal("3.5"),
                "carbs_per_100": Decimal("4.7"),
                "fat_per_100": Decimal("3.3"),
                "is_basic": True,
                "available_quantity": 3,
                "minimum_quantity": 5,
            },
            {
                "name": "Извара",
                "brand": "",
                "category": Product.CATEGORY_MILK_CHEESE,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 98,
                "protein_per_100": Decimal("11.0"),
                "carbs_per_100": Decimal("3.4"),
                "fat_per_100": Decimal("4.3"),
                "is_basic": False,
                "available_quantity": 2,
                "minimum_quantity": 3,
            },
            {
                "name": "Кашкавал",
                "brand": "",
                "category": Product.CATEGORY_MILK_CHEESE,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 356,
                "protein_per_100": Decimal("24.0"),
                "carbs_per_100": Decimal("2.0"),
                "fat_per_100": Decimal("28.0"),
                "is_basic": False,
                "available_quantity": 500,
                "minimum_quantity": 300,
            },
            {
                "name": "Ориз",
                "brand": "",
                "category": Product.CATEGORY_GRAINS_LEGUMES,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 360,
                "protein_per_100": Decimal("7.0"),
                "carbs_per_100": Decimal("79.0"),
                "fat_per_100": Decimal("0.6"),
                "is_basic": True,
                "available_quantity": 700,
                "minimum_quantity": 500,
            },
            {
                "name": "Овесени ядки",
                "brand": "",
                "category": Product.CATEGORY_GRAINS_LEGUMES,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 389,
                "protein_per_100": Decimal("17.0"),
                "carbs_per_100": Decimal("66.0"),
                "fat_per_100": Decimal("7.0"),
                "is_basic": True,
                "available_quantity": 2,
                "minimum_quantity": 1,
            },
            {
                "name": "Леща",
                "brand": "",
                "category": Product.CATEGORY_GRAINS_LEGUMES,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 352,
                "protein_per_100": Decimal("24.0"),
                "carbs_per_100": Decimal("60.0"),
                "fat_per_100": Decimal("1.1"),
                "is_basic": False,
                "available_quantity": 0,
                "minimum_quantity": 500,
            },
            {
                "name": "Банан",
                "brand": "",
                "category": Product.CATEGORY_FRUIT_VEGETABLES,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 89,
                "protein_per_100": Decimal("1.1"),
                "carbs_per_100": Decimal("23.0"),
                "fat_per_100": Decimal("0.3"),
                "is_basic": False,
                "available_quantity": 3,
                "minimum_quantity": 6,
            },
            {
                "name": "Ябълка",
                "brand": "",
                "category": Product.CATEGORY_FRUIT_VEGETABLES,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 52,
                "protein_per_100": Decimal("0.3"),
                "carbs_per_100": Decimal("14.0"),
                "fat_per_100": Decimal("0.2"),
                "is_basic": False,
                "available_quantity": 5,
                "minimum_quantity": 6,
            },
            {
                "name": "Домати",
                "brand": "",
                "category": Product.CATEGORY_FRUIT_VEGETABLES,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 18,
                "protein_per_100": Decimal("0.9"),
                "carbs_per_100": Decimal("3.9"),
                "fat_per_100": Decimal("0.2"),
                "is_basic": True,
                "available_quantity": 300,
                "minimum_quantity": 400,
            },
            {
                "name": "Краставици",
                "brand": "",
                "category": Product.CATEGORY_FRUIT_VEGETABLES,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 15,
                "protein_per_100": Decimal("0.7"),
                "carbs_per_100": Decimal("3.6"),
                "fat_per_100": Decimal("0.1"),
                "is_basic": True,
                "available_quantity": 250,
                "minimum_quantity": 300,
            },
            {
                "name": "Авокадо",
                "brand": "",
                "category": Product.CATEGORY_FRUIT_VEGETABLES,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 160,
                "protein_per_100": Decimal("2.0"),
                "carbs_per_100": Decimal("9.0"),
                "fat_per_100": Decimal("15.0"),
                "is_basic": False,
                "available_quantity": 1,
                "minimum_quantity": 2,
            },
            {
                "name": "Фъстъчено масло",
                "brand": "",
                "category": Product.CATEGORY_NUTS_OILS,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 588,
                "protein_per_100": Decimal("25.0"),
                "carbs_per_100": Decimal("20.0"),
                "fat_per_100": Decimal("50.0"),
                "is_basic": False,
                "available_quantity": 1,
                "minimum_quantity": 1,
            },
            {
                "name": "Зехтин",
                "brand": "",
                "category": Product.CATEGORY_NUTS_OILS,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 884,
                "protein_per_100": Decimal("0.0"),
                "carbs_per_100": Decimal("0.0"),
                "fat_per_100": Decimal("100.0"),
                "is_basic": True,
                "available_quantity": 2,
                "minimum_quantity": 1,
            },
            {
                "name": "Черен шоколад",
                "brand": "",
                "category": Product.CATEGORY_DESSERTS_SWEETS,
                "unit": Product.UNIT_GRAMS,
                "calories_per_100": 546,
                "protein_per_100": Decimal("4.9"),
                "carbs_per_100": Decimal("61.0"),
                "fat_per_100": Decimal("31.0"),
                "is_basic": False,
                "available_quantity": 0,
                "minimum_quantity": 200,
            },
            {
                "name": "Минерална вода",
                "brand": "",
                "category": Product.CATEGORY_DRINKS,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 0,
                "protein_per_100": Decimal("0.0"),
                "carbs_per_100": Decimal("0.0"),
                "fat_per_100": Decimal("0.0"),
                "is_basic": True,
                "available_quantity": 2,
                "minimum_quantity": 6,
            },
            {
                "name": "Протеинов бар",
                "brand": "",
                "category": Product.CATEGORY_PACKAGED_STORE,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 370,
                "protein_per_100": Decimal("30.0"),
                "carbs_per_100": Decimal("35.0"),
                "fat_per_100": Decimal("10.0"),
                "is_basic": False,
                "available_quantity": 2,
                "minimum_quantity": 4,
            },
            {
                "name": "Черен пипер",
                "brand": "",
                "category": Product.CATEGORY_SPICES,
                "unit": Product.UNIT_PIECES,
                "calories_per_100": 251,
                "protein_per_100": Decimal("10.0"),
                "carbs_per_100": Decimal("64.0"),
                "fat_per_100": Decimal("3.3"),
                "is_basic": False,
                "available_quantity": 1,
                "minimum_quantity": 1,
            },
        ]

        product_objects = {}
        for item in products_data:
            product, _ = Product.objects.get_or_create(
                name=item["name"],
                brand=item["brand"],
                defaults={
                    "category": item["category"],
                    "unit": item["unit"],
                    "calories_per_100": item["calories_per_100"],
                    "protein_per_100": item["protein_per_100"],
                    "carbs_per_100": item["carbs_per_100"],
                    "fat_per_100": item["fat_per_100"],
                    "is_basic": item["is_basic"],
                },
            )

            # ако съществува, update-ваме стойностите
            product.category = item["category"]
            product.unit = item["unit"]
            product.calories_per_100 = item["calories_per_100"]
            product.protein_per_100 = item["protein_per_100"]
            product.carbs_per_100 = item["carbs_per_100"]
            product.fat_per_100 = item["fat_per_100"]
            product.is_basic = item["is_basic"]
            product.save()

            Inventory.objects.update_or_create(
                product=product,
                defaults={
                    "available_quantity": item["available_quantity"],
                    "minimum_quantity": item["minimum_quantity"],
                },
            )

            product_objects[item["name"]] = product

        self.stdout.write(self.style.SUCCESS("Създадени са 20 продукта и наличности."))

        self.stdout.write("Създавам demo ястия...")

        dishes_data = [
            {"name": "Омлет", "calories": 320, "protein": Decimal("22.0"), "carbs": Decimal("3.0"), "fat": Decimal("24.0"), "note": "Закуска с яйца и сирене"},
            {"name": "Овесена каша", "calories": 410, "protein": Decimal("18.0"), "carbs": Decimal("54.0"), "fat": Decimal("13.0"), "note": "С банан и фъстъчено масло"},
            {"name": "Пилешко с ориз", "calories": 560, "protein": Decimal("45.0"), "carbs": Decimal("52.0"), "fat": Decimal("14.0"), "note": "Класически обяд"},
            {"name": "Салата с авокадо", "calories": 290, "protein": Decimal("6.0"), "carbs": Decimal("18.0"), "fat": Decimal("21.0"), "note": "Лека вечеря"},
            {"name": "Сьомга с домати", "calories": 470, "protein": Decimal("34.0"), "carbs": Decimal("8.0"), "fat": Decimal("32.0"), "note": "Богата на мазнини и протеин"},
            {"name": "Извара с ябълка", "calories": 240, "protein": Decimal("18.0"), "carbs": Decimal("20.0"), "fat": Decimal("8.0"), "note": "Бързо междинно хранене"},
            {"name": "Леща яхния", "calories": 430, "protein": Decimal("24.0"), "carbs": Decimal("58.0"), "fat": Decimal("8.0"), "note": "Растителен обяд"},
            {"name": "Протеинова закуска", "calories": 350, "protein": Decimal("30.0"), "carbs": Decimal("22.0"), "fat": Decimal("12.0"), "note": "Подходяща след тренировка"},
            {"name": "Пилешка салата", "calories": 390, "protein": Decimal("36.0"), "carbs": Decimal("10.0"), "fat": Decimal("21.0"), "note": "Лек и засищащ вариант"},
            {"name": "Ориз с яйца", "calories": 500, "protein": Decimal("21.0"), "carbs": Decimal("60.0"), "fat": Decimal("18.0"), "note": "Бърз dinner prep"},
        ]

        dish_objects = {}
        for item in dishes_data:
            dish, _ = Dish.objects.update_or_create(
                name=item["name"],
                defaults={
                    "calories": item["calories"],
                    "protein": item["protein"],
                    "carbs": item["carbs"],
                    "fat": item["fat"],
                    "note": item["note"],
                },
            )
            dish_objects[item["name"]] = dish

        self.stdout.write(self.style.SUCCESS("Създадени са 10 ястия."))

        self.stdout.write("Създавам demo седмично меню...")

        monday = date.today() - timedelta(days=date.today().weekday())
        week_menu, _ = WeekMenu.objects.update_or_create(
            start_date=monday,
            defaults={"notes": "Примерно седмично меню за презентация на проекта"},
        )

        Meal.objects.filter(week_menu=week_menu).delete()

        meals_data = [
            # Monday
            {"day": 1, "dish": "Овесена каша", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 1, "dish": "Пилешко с ориз", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 1, "dish": None, "product": "Банан", "quantity": 1, "notes": "Следобедна закуска"},
            # Tuesday
            {"day": 2, "dish": "Омлет", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 2, "dish": None, "product": "Кисело мляко", "quantity": 200, "notes": "Междинно"},
            {"day": 2, "dish": "Сьомга с домати", "product": None, "quantity": 1, "notes": "Вечеря"},
            # Wednesday
            {"day": 3, "dish": "Протеинова закуска", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 3, "dish": "Леща яхния", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 3, "dish": None, "product": "Ябълка", "quantity": 1, "notes": "Следобед"},
            # Thursday
            {"day": 4, "dish": "Извара с ябълка", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 4, "dish": "Пилешка салата", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 4, "dish": None, "product": "Протеинов бар", "quantity": 1, "notes": "Snack"},
            # Friday
            {"day": 5, "dish": "Овесена каша", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 5, "dish": "Ориз с яйца", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 5, "dish": None, "product": "Банан", "quantity": 1, "notes": "След тренировка"},
            # Saturday
            {"day": 6, "dish": "Омлет", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 6, "dish": "Салата с авокадо", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 6, "dish": None, "product": "Черен шоколад", "quantity": 30, "notes": "Десерт"},
            # Sunday
            {"day": 7, "dish": "Протеинова закуска", "product": None, "quantity": 1, "notes": "Закуска"},
            {"day": 7, "dish": "Пилешко с ориз", "product": None, "quantity": 1, "notes": "Обяд"},
            {"day": 7, "dish": None, "product": "Авокадо", "quantity": 1, "notes": "Вечеря / добавка"},
        ]

        for item in meals_data:
            Meal.objects.create(
                week_menu=week_menu,
                day=item["day"],
                dish=dish_objects[item["dish"]] if item["dish"] else None,
                product=product_objects[item["product"]] if item["product"] else None,
                quantity=item["quantity"],
                notes=item["notes"],
            )

        self.stdout.write(self.style.SUCCESS("Създадено е 1 седмично меню с демо записи."))
        self.stdout.write(self.style.SUCCESS("Готово. Изпълни: python manage.py seed_demo_data --reset"))