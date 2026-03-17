    # PlatePlotter

    PlatePlotter е Django уеб приложение за планиране на седмично меню, управление на хранителни продукти и следене на наличности у дома.

    Проектът е разработен като изпитен проект за **Django Basics @ SoftUni**.

    ---

    ## Основни функционалности

    - управление на хранителни продукти
    - следене на наличности и минимални количества
    - създаване на ястия
    - планиране на седмично меню
    - добавяне на хранения по дни
    - автоматично изчисляване на калории и макронутриенти

    ---

    ## Технологии

    - Python
    - Django
    - PostgreSQL
    - Bootstrap
    - Django Template Engine

    ---

    ## Структура на проекта

    Проектът съдържа три Django приложения:

    - **inventory** – управление на продукти и наличности  
    - **meals** – управление на ястия  
    - **weekmenu** – седмично меню и хранения  

    ---

    ## Основни модели

    - Product
    - Inventory
    - Dish
    - DishIngredient
    - WeekMenu
    - Meal

    ---

    ## Инсталация

    Клонирай проекта:

    ```bash
    git clone https://github.com/AlexanderHrHristov/plate-plotter.git
    cd plate-plotter

    Създай виртуална среда:

    python -m venv .venv

    Активирай я:

    Windows

    .venv\Scripts\activate

    Инсталирай зависимостите:

    pip install -r requirements.txt
    Настройка на базата данни

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
    Проектът съдържа custom management command за генериране на примерни данни:
    python manage.py seed_demo_data

    Командата създава:
    примерни продукти
    наличности
    ястия
    седмично меню
    хранения

    Стартиране на приложението
    python manage.py runserver

    Отвори: http://127.0.0.1:8000/
    Автор:  Alexander Hristov
    Django  Basics Retake Exam Project – SoftUni
