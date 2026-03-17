from django import forms
from .models import Product, Inventory


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Например: Кисело мляко"}),
            "brand": forms.TextInput(attrs={"placeholder": "Марка / Производител"}),
            "category": forms.Select(),
            "unit": forms.Select(),
            "calories_per_100": forms.NumberInput(attrs={"placeholder": "Калории на 100 g/ml"}),
            "protein_per_100": forms.NumberInput(attrs={"placeholder": "Белтъчини на 100 g/ml"}),
            "carbs_per_100": forms.NumberInput(attrs={"placeholder": "Въглехидрати на 100 g/ml"}),
            "fat_per_100": forms.NumberInput(attrs={"placeholder": "Мазнини на 100 g/ml"}),
        }
        help_texts = {
            "name": "Въведи име на продукта така, както ще се показва в менюто и наличностите.",
            "minimum_quantity": "Под това количество продуктът ще се счита за почти изчерпан.",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Името на продукта трябва да съдържа поне 2 символа.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        protein = cleaned_data.get("protein_per_100")
        carbs = cleaned_data.get("carbs_per_100")
        fat = cleaned_data.get("fat_per_100")
        calories = cleaned_data.get("calories_per_100")

        numeric_fields = {
            "Белтъчини": protein,
            "Въглехидрати": carbs,
            "Мазнини": fat,
            "Калории": calories,
        }

        for field_name, value in numeric_fields.items():
            if value is not None and value < 0:
                raise forms.ValidationError(f"{field_name} не може да бъде отрицателна стойност.")

        return cleaned_data


class InventoryListForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
        labels = {
            "available_quantity": "Налично количество",
            "minimum_quantity": "Минимално количество",
        }

    def clean(self):
        cleaned_data = super().clean()
        available_quantity = cleaned_data.get("available_quantity")
        minimum_quantity = cleaned_data.get("minimum_quantity")

        if available_quantity is not None and available_quantity < 0:
            self.add_error("available_quantity", "Наличното количество не може да е отрицателно.")

        if minimum_quantity is not None and minimum_quantity < 0:
            self.add_error("minimum_quantity", "Минималното количество не може да е отрицателно.")

        return cleaned_data


class InventoryStockUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["available_quantity", "minimum_quantity"]

    def clean(self):
        cleaned_data = super().clean()
        available_quantity = cleaned_data.get("available_quantity")
        minimum_quantity = cleaned_data.get("minimum_quantity")

        # Тази форма се използва само за актуализация на наличности у дома, не трябва да има отрицателни стойности.
        if available_quantity is not None and available_quantity < 0:
            self.add_error("available_quantity", "Количеството не може да бъде отрицателно.")

        if minimum_quantity is not None and minimum_quantity < 0:
            self.add_error("minimum_quantity", "Минималното количество не може да бъде отрицателно.")

        return cleaned_data


class ProductDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label="Потвърждавам, че искам да изтрия продукта",
        error_messages={
            "required": "Трябва да потвърдите изтриването."
        }
    )