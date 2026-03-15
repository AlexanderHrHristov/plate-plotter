from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import DishForm, RecipeItemForm
from .models import Dish, RecipeItem


class DishListView(ListView):
    model = Dish
    template_name = "meals/dish-list.html"
    context_object_name = "dishes"


class DishDetailView(DetailView):
    model = Dish
    template_name = "meals/dish-detail.html"
    context_object_name = "dish"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_items"] = self.object.recipeitem_set.select_related("product")
        return context


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


class RecipeItemCreateView(CreateView):
    model = RecipeItem
    form_class = RecipeItemForm
    template_name = "meals/recipeitem-create.html"
    success_url = reverse_lazy("dish-list")


class RecipeItemUpdateView(UpdateView):
    model = RecipeItem
    form_class = RecipeItemForm
    template_name = "meals/recipeitem-edit.html"
    success_url = reverse_lazy("dish-list")


class RecipeItemDeleteView(DeleteView):
    model = RecipeItem
    template_name = "meals/recipeitem-delete.html"
    success_url = reverse_lazy("dish-list")

# Create your views here.
