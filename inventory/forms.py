from django import forms
from .models import Product, Inventory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Продукт"}),
            "brand": forms.TextInput(attrs={"placeholder": "Марка / Производител"}),
            "category": forms.Select(),
            "unit": forms.Select(),
            "calories_per_100": forms.NumberInput(attrs={"placeholder": "Калории / 100g"}),
            "protein_per_100": forms.NumberInput(attrs={"placeholder": "Белтъчини / 100g", "step": "0.01"}),
            "carbs_per_100": forms.NumberInput(attrs={"placeholder": "Въглехидрати / 100g", "step": "0.01"}),
            "fat_per_100": forms.NumberInput(attrs={"placeholder": "Мазнини / 100g", "step": "0.01"}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryEditForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["available_quantity", "minimum_quantity"]


class DeleteProductForm(forms.Form):
    confirm = forms.BooleanField(label="Потвърди изтриването на продукта")