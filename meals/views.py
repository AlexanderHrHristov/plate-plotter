from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import DishForm
from .models import Dish


class DishListView(ListView):
    model = Dish
    template_name = "meals/dish-list.html"
    context_object_name = "dishes"
    queryset = Dish.objects.order_by("name")


class DishDetailView(DetailView):
    model = Dish
    template_name = "meals/dish-detail.html"
    context_object_name = "dish"


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = "meals/dish-create.html"
    success_url = reverse_lazy("dish-list")


class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "meals/dish-edit.html"
    success_url = reverse_lazy("dish-list")


class DishDeleteView(DeleteView):
    model = Dish
    template_name = "meals/dish-delete.html"
    success_url = reverse_lazy("dish-list")