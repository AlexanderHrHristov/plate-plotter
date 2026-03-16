from django.urls import path

from .views import (
    WeekMenuListView,
    WeekMenuDetailView,
    WeekMenuCreateView,
    WeekMenuUpdateView,
    WeekMenuDeleteView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
)

urlpatterns = [
    path("weekmenus/", WeekMenuListView.as_view(), name="weekmenu-list"),
    path("weekmenus/create/", WeekMenuCreateView.as_view(), name="weekmenu-create"),
    path("weekmenus/<int:pk>/", WeekMenuDetailView.as_view(), name="weekmenu-detail"),
    path("weekmenus/<int:pk>/edit/", WeekMenuUpdateView.as_view(), name="weekmenu-edit"),
    path("weekmenus/<int:pk>/delete/", WeekMenuDeleteView.as_view(), name="weekmenu-delete"),

    path("meals/create/", MealCreateView.as_view(), name="meal-create"),
    path("meals/<int:pk>/edit/", MealUpdateView.as_view(), name="meal-edit"),
    path("meals/<int:pk>/delete/", MealDeleteView.as_view(), name="meal-delete"),
]