from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def step_num(value):
    """
    1.0 -> "1"
    1.5 -> "1.5"
    """
    if value is None:
        return ""
    d = Decimal(str(value))
    s = format(d.normalize(), "f").rstrip("0").rstrip(".")
    return s
