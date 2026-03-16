from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    InventoryListView,
    InventoryUpdateView,
    ShoppingListView
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product-edit"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),

    path("inventory/", InventoryListView.as_view(), name="inventory-list"),
    path("inventory/<int:pk>/edit/", InventoryUpdateView.as_view(), name="inventory-edit"),
    path("shopping-list/", ShoppingListView.as_view(), name="shopping-list"),
]