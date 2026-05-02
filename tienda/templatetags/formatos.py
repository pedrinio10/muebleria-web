from django import template

register = template.Library()

@register.filter
def precio_ar(value):
    try:
        return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return value