from django import forms
from .models import Dish


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "calories", "protein", "carbs", "fat", "note"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ястие"}),
            "calories": forms.NumberInput(attrs={"placeholder": "Калории"}),
            "protein": forms.NumberInput(attrs={"placeholder": "Белтъчини", "step": "0.01"}),
            "carbs": forms.NumberInput(attrs={"placeholder": "Въглехидрати", "step": "0.01"}),
            "fat": forms.NumberInput(attrs={"placeholder": "Мазнини", "step": "0.01"}),
            "note": forms.TextInput(attrs={"placeholder": "Кратка бележка"}),
        }