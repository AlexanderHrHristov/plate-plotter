from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import WeekMenuForm, MealForm
from .models import WeekMenu, Meal


class WeekMenuListView(ListView):
    model = WeekMenu
    template_name = "weekmenu/weekmenu-list.html"
    context_object_name = "weekmenus"


class WeekMenuDetailView(DetailView):
    model = WeekMenu
    template_name = "weekmenu/weekmenu-detail.html"
    context_object_name = "weekmenu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        days_data = []
        for day_value, day_label in Meal.DAY_CHOICES:
            day_meals = self.object.meals.filter(day=day_value)

            days_data.append({
                "value": day_value,
                "label": day_label,
                "meals": day_meals,
                "calories": self.object.total_calories_for_day(day_value),
                "protein": self.object.total_protein_for_day(day_value),
                "carbs": self.object.total_carbs_for_day(day_value),
                "fat": self.object.total_fat_for_day(day_value),
            })

        context["days_data"] = days_data
        context["week_calories"] = self.object.total_calories_for_week()
        context["week_protein"] = self.object.total_protein_for_week()
        context["week_carbs"] = self.object.total_carbs_for_week()
        context["week_fat"] = self.object.total_fat_for_week()

        return context


class WeekMenuCreateView(CreateView):
    model = WeekMenu
    form_class = WeekMenuForm
    template_name = "weekmenu/weekmenu-create.html"
    success_url = reverse_lazy("weekmenu-list")


class WeekMenuUpdateView(UpdateView):
    model = WeekMenu
    form_class = WeekMenuForm
    template_name = "weekmenu/weekmenu-edit.html"
    success_url = reverse_lazy("weekmenu-list")


class WeekMenuDeleteView(DeleteView):
    model = WeekMenu
    template_name = "weekmenu/weekmenu-delete.html"
    success_url = reverse_lazy("weekmenu-list")


class MealCreateView(CreateView):
    model = Meal
    form_class = MealForm
    template_name = "weekmenu/meal-create.html"

    def get_initial(self):
        initial = super().get_initial()
        weekmenu_id = self.request.GET.get("weekmenu")
        if weekmenu_id:
            initial["week_menu"] = weekmenu_id
        return initial

    def get_success_url(self):
        return reverse_lazy("weekmenu-detail", kwargs={"pk": self.object.week_menu.pk})


class MealUpdateView(UpdateView):
    model = Meal
    form_class = MealForm
    template_name = "weekmenu/meal-edit.html"

    def get_success_url(self):
        return reverse_lazy("weekmenu-detail", kwargs={"pk": self.object.week_menu.pk})


class MealDeleteView(DeleteView):
    model = Meal
    template_name = "weekmenu/meal-delete.html"

    def get_success_url(self):
        return reverse_lazy("weekmenu-detail", kwargs={"pk": self.object.week_menu.pk})