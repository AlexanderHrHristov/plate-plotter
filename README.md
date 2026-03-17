PlatePlotter

PlatePlotter е Django уеб приложение за планиране на седмично меню, управление на хранителни продукти и следене на наличности у дома.
Проектът е разработен като изпитен проект за Django Basics @ SoftUni.

  
 ОСНОВНИ ФУНКЦИОНАЛНОСТИ  

    - управление на хранителни продукти
    - следене на наличности и минимални количества
    - създаване на ястия
    - планиране на седмично меню
    - добавяне на хранения по дни
    - автоматично изчисляване на калории и макронутриенти


ИЗПОЛЗВАНИ ТЕХНОЛОГИИ

    - Python
    - Django
    - PostgreSQL
    - Bootstrap
    - Django Template Engine


СТРУКТУРА

    Проектът съдържа три Django приложения:
    - inventory – управление на продукти и наличности  
    - meals – управление на ястия  
    - weekmenu – седмично меню и хранения  


    Основните модели на проекта са:
    - Product
    - Inventory
    - Dish
    - Meal
    - WeekMenu


ИНСТАЛАЦИЯ    

    Клонирайте проекта от GitHub хранилището:
    git clone https://github.com/AlexanderHrHristov/plate-plotter.git

    Отворете директория:
    cd plate-plotter

    Създайте виртуална среда:
    python -m venv .venv

    Активиране:
    .venv\Scripts\activate

    Инсталиране на зависимостите:
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
    
    Изпълнете миграции:
    python manage.py makemigrations
    python manage.py migrate



 ДЕМО ДАННИ

    Проектът съдържа custom management command за генериране на примерни данни:
    python manage.py seed_demo_data

    Командата създава:
    -    примерни продукти
    -    наличности
    -    ястия
    -   седмично меню
    -   списък за пазаруване

    Стартиране на приложението
    python manage.py runserver

    Отвори: http://127.0.0.1:8000/


Автор на  проекта: Alexander Hristov
            https://github.com/AlexanderHrHristov
            email: alexander.hristov@proton.me
            https://www.linkedin.com/in/alexander-hristov-82b92821/
            phone: +359889125661


