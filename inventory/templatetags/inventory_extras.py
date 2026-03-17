from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def stock_status(available_quantity, minimum_quantity):
    if available_quantity is None:
        return "Няма данни"

    available_quantity = Decimal(available_quantity)
    minimum_quantity = Decimal(minimum_quantity)

    if available_quantity == 0:
        return "Изчерпан"
    if available_quantity < minimum_quantity:
        return "Под минимум"
    return "Наличен"


@register.filter(name="stock_badge")
def stock_badge_class(available_quantity, minimum_quantity):
    if available_quantity is None:
        return "bg-secondary"

    available_quantity = Decimal(available_quantity)
    minimum_quantity = Decimal(minimum_quantity)

    if available_quantity == 0:
        return "bg-dark"
    if available_quantity < minimum_quantity:
        return "bg-danger"
    return "bg-success"