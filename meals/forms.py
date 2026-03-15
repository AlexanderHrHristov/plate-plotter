from django import forms
from .models import Dish, RecipeItem


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "description"]   # НЕ '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ястие"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class RecipeItemForm(forms.ModelForm):
    class Meta:
        model = RecipeItem
        fields = "__all__"
        widgets = {
            "quantity_needed": forms.NumberInput(attrs={"placeholder": "Необходимо количество"}),
            "note": forms.TextInput(attrs={"placeholder": "Бележка"}),
        }


class DeleteRecipeItemForm(forms.Form):
    confirm = forms.BooleanField(label="Потвърди изтриването на продукта от рецептата")