from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from decimal import Decimal
from .forms import ProductCreateForm, InventoryStockUpdateForm
from .models import Product, Inventory
from django.db import models



class ProductListView(ListView): # Показва списък с продукти като querryset.
    model = Product
    template_name = "inventory/product-list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.order_by("name", "brand")
        category = self.request.GET.get("category")

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_category"] = self.request.GET.get("category", "")
        context["category_choices"] = Product.CATEGORY_CHOICES
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "inventory/product-detail.html"
    context_object_name = "product"

class ProductCreateView(CreateView): 
    model = Product
    form_class = ProductCreateForm
    template_name = "inventory/product-create.html"
    success_url = reverse_lazy("product-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        Inventory.objects.get_or_create(
            product=self.object,
            defaults={
                "available_quantity": 0,
                "minimum_quantity": 0,
            },
        )
        return response




class ProductUpdateView(UpdateView): # Ъпдейтване на продукта
    model = Product
    form_class = ProductCreateForm
    template_name = "inventory/product-edit.html"
    success_url = reverse_lazy("product-list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "inventory/product-delete.html"
    success_url = reverse_lazy("product-list")


class InventoryListView(ListView):
    model = Inventory
    template_name = "inventory/inventory-list.html"
    context_object_name = "inventory_items"
    queryset = Inventory.objects.select_related("product").order_by("product__name", "product__brand")


class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryStockUpdateForm
    template_name = "inventory/inventory-edit.html"
    success_url = reverse_lazy("inventory-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.object.product
        return context
    
"""
Генеративен шопинг лист - прави списък от продукти, 
чиито запас е паднал под налично к-во. 
"""

from django.db import models
from django.views.generic import ListView

from .models import Inventory
from weekmenu.models import WeekMenuModel



class ShoppingListView(ListView):
    template_name = "inventory/shopping-list.html"
    context_object_name = "shopping_items"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shopping_items = []
        week_menu_id = self.request.GET.get("week_menu")

        context["week_menus"] = WeekMenuModel.objects.all().order_by("-start_date")

        if not week_menu_id:
            context["shopping_items"] = []
            context["selected_week_menu"] = None
            context["total_items"] = 0
            return context

        try:
            selected_week_menu = WeekMenuModel.objects.get(pk=week_menu_id)
        except WeekMenuModel.DoesNotExist:
            context["shopping_items"] = []
            context["selected_week_menu"] = None
            context["total_items"] = 0
            return context

        inventory_items = Inventory.objects.select_related("product")
        inventory_map = {item.product_id: item for item in inventory_items}

        # Продукти под минималната наличност
        for inventory_item in inventory_items:
            if inventory_item.is_below_minimum:
                shopping_items.append({
                    "product": inventory_item.product,
                    "available_quantity": inventory_item.available_quantity,
                    "minimum_quantity": inventory_item.minimum_quantity,
                    "needed_for_week": 0,
                    "quantity_to_buy": inventory_item.shortage_amount,
                    "reason": "Под минимална наличност",
                })

        # Продукти, които фигурират директно в седмичното меню
        weekly_product_needs = {}
        weekly_meals = selected_week_menu.meals.filter(product__isnull=False).select_related("product")

        for meal in weekly_meals:
            product_id = meal.product.id
            if product_id not in weekly_product_needs:
                weekly_product_needs[product_id] = {
                    "product": meal.product,
                    "needed_quantity": Decimal("0"),
                }
            weekly_product_needs[product_id]["needed_quantity"] += meal.quantity

        for product_id, data in weekly_product_needs.items():
            product = data["product"]
            needed_quantity = data["needed_quantity"]

            inventory_item = inventory_map.get(product_id)
            available_quantity = inventory_item.available_quantity if inventory_item else Decimal("0")
            minimum_quantity = inventory_item.minimum_quantity if inventory_item else Decimal("0")

            if needed_quantity > available_quantity:
                quantity_to_buy = needed_quantity - available_quantity

                existing = next((x for x in shopping_items if x["product"].id == product_id), None)
                if existing:
                    existing["needed_for_week"] = needed_quantity
                    existing["quantity_to_buy"] = max(existing["quantity_to_buy"], quantity_to_buy)
                    existing["reason"] = "Под минимум + нужен за седмицата"
                else:
                    shopping_items.append({
                        "product": product,
                        "available_quantity": available_quantity,
                        "minimum_quantity": minimum_quantity,
                        "needed_for_week": needed_quantity,
                        "quantity_to_buy": quantity_to_buy,
                        "reason": "Нужен за седмицата",
                    })

        context["shopping_items"] = shopping_items
        context["selected_week_menu"] = selected_week_menu
        context["total_items"] = len(shopping_items)

        return context