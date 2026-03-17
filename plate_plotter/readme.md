# PlatePlotter

PlatePlotter е Django уеб приложение за планиране на седмично меню, управление на хранителни продукти и следене на наличности у дома.
Проектът е разработен като изпитен проект за Django Basics @ SoftUni.
Основни функционалности
- управление на хранителни продукти
- следене на наличности и минимални количества
- създаване на ястия
- аниране на седмично меню

завяне на хранения по дни
автоматично изчисляване на калории и макронутриенти
генериране на списък за пазаруване
Технологии
Python
Django
PostgreSQL
Bootstrap
Django Template Engine
Структура на проекта
Проектът съдържа три Django приложения:
inventory – управление на продукти и наличности
meals – управление на ястия и съставки
weekmenu – седмично меню и хранения

Основни модели
Product
Inventory
Dish
DishIngredient (Many-to-Many между Dish и Product)
WeekMenu
Meal

*** УКАЗАНИЯ ЗА ИНСТАЛИРАНЕ НА ПРОДУКТА ***

1. Клониране на проекта от Public GitHub хранилище:

git clone https://github.com/AlexanderHrHristov/plate-plotter.git
cd plate-plotter

Създай виртуална среда:

python -m venv .venv

Активиране:
за Windows
.venv\Scripts\activate

Инсталирана на зависимостите:

pip install -r requirements.txt
Настройка на базата

Проектът използва PostgreSQL.

Примерна конфигурация в settings.py:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "plateplotter",
        "USER": "postgres",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
Миграции
python manage.py makemigrations
python manage.py migrate
Демо данни

Проектът включва custom management command за генериране на примерни данни:

python manage.py seed_demo_data

Това ще създаде примерни:

продукти

наличности

ястия

седмично меню

хранения

Стартиране
python manage.py runserver

Отвори:

http://127.0.0.1:8000/
Автор

Alexander Hristov
Django Basics Retake Exam Project – SoftUni



