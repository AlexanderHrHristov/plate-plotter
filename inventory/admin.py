from django.contrib import admin
from .models import Product, Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "unit",
        "calories_per_100",
        "protein_per_100",
        "carbs_per_100",
        "fat_per_100",
        "is_basic",
    )

    list_filter = (
        "category",
        "unit",
        "is_basic",
    )

    search_fields = (
        "name",
        "brand",
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "available_quantity",
        "minimum_quantity",
        "is_below_minimum",
    )

    search_fields = (
        "product__name",
        "product__brand",
    )