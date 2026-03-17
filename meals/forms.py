from django import forms
from .models import Dish


class DishCreateForm(forms.ModelForm): # Форма за ястия - съдържа и макросите за всяко от тях - изчислява калориите на храненията в седмичното меню.
    class Meta:
        model = Dish
        fields = ["name", "calories", "protein", "carbs", "fat", "note"]

        labels = {
            "name": "Име на ястието",
            "calories": "Калории",
            "protein": "Белтъчини",
            "carbs": "Въглехидрати",
            "fat": "Мазнини",
            "note": "Бележка",
        }

        help_texts = {
            "calories": "Общо калории за порция.",
            "protein": "Количество белтъчини в грамове.",
            "carbs": "Количество въглехидрати в грамове.",
            "fat": "Количество мазнини в грамове.",
        }

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ястие"}),
            "calories": forms.NumberInput(attrs={"placeholder": "Калории за порция"}),
            "protein": forms.NumberInput(attrs={"placeholder": "Белтъчини (г)", "step": "0.1"}),
            "carbs": forms.NumberInput(attrs={"placeholder": "Въглехидрати (г)", "step": "0.1"}),
            "fat": forms.NumberInput(attrs={"placeholder": "Мазнини (г)", "step": "0.1"}),
            "note": forms.TextInput(attrs={"placeholder": "Забележка"}),
        }

def clean_name(self):
    name = self.cleaned_data["name"].strip()

    if len(name) < 2:
        raise forms.ValidationError(
            "Името на ястието трябва да съдържа поне 2 символа."
        )

    return name