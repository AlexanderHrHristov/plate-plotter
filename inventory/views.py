from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, InventoryEditForm
from .models import Product, Inventory


class ProductListView(ListView):
    model = Product
    template_name = "inventory/product-list.html"
    context_object_name = "products"
    queryset = Product.objects.order_by("name", "brand")


class ProductDetailView(DetailView):
    model = Product
    template_name = "inventory/product-detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
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
    form_class = InventoryEditForm
    template_name = "inventory/inventory-edit.html"
    success_url = reverse_lazy("inventory-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.object.product
        return context