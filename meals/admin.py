from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "calories", "protein", "carbs", "fat")
    search_fields = ("name", "note")