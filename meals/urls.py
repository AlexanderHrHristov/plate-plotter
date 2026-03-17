from django.urls import path

from .views import (
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
)

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),  # url-тата за ястията - da проверя дали работи int:pk!
    path("dishes/<int:pk>/edit/", DishUpdateView.as_view(), name="dish-edit"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
] 