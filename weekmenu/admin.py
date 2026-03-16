from django.contrib import admin
from .models import WeekMenu, Meal


class MealInline(admin.TabularInline):
    model = Meal
    extra = 1


@admin.register(WeekMenu)
class WeekMenuAdmin(admin.ModelAdmin):
    list_display = ("start_date", "notes")
    search_fields = ("start_date",)
    inlines = [MealInline]


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("week_menu", "day", "dish", "product", "quantity")
    list_filter = ("day",)