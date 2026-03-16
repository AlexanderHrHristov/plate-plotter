from django import forms
from .models import WeekMenu, Meal


class WeekMenuForm(forms.ModelForm):
    class Meta:
        model = WeekMenu
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = "__all__"
        widgets = {
            "quantity": forms.NumberInput(attrs={"placeholder": "Количество"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class DeleteMealForm(forms.Form):
    confirm = forms.BooleanField(label="Потвърди изтриването на записа")