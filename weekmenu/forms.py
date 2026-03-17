from django import forms

from .models import WeekMenuModel, Meal




class WeeklyMenuPlannerForm(forms.ModelForm): #   Форма за създаване или редакция на седмичното меню.

    class Meta:
        model = WeekMenuModel
        fields = ["start_date", "notes"]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }



    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]

        if WeekMenuModel.objects.filter(start_date=start_date).exists():
            raise forms.ValidationError(
                "Вече има меню, което започва на тази дата."
            )

        return start_date


class MyMealForm(forms.ModelForm): # Форма за добавяне на хранене в седмично меню.

    class Meta:
        model = Meal
        fields = [
            "week_menu",
            "day",
            "dish",
            "product",
            "quantity",
            "notes",
        ]

        widgets = {
            "quantity": forms.NumberInput(attrs={"placeholder": "Количество"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["dish"].empty_label = "Избери ястие"
        self.fields["product"].empty_label = "Избери продукт"

    def clean(self):
        cleaned_data = super().clean()
        dish = cleaned_data.get("dish")
        product = cleaned_data.get("product")

        if not dish and not product:
            raise forms.ValidationError(
                "Трябва да изберете или ястие, или продукт."
            )

        if dish and product:
            raise forms.ValidationError(
                "Може да изберете само едно от ястие или продукт."
            )

        return cleaned_data


class DeleteMyMealForm(forms.Form):
    confirm = forms.BooleanField(
        label="Изтриване на записа"
    )