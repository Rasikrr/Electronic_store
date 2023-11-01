from django import template

# Create your views here.

register = template.Library()
# template operations


@register.filter(name="mul")
def mul(value, arg):
    return value*arg

@register.filter(name="filter")
def filter():
    return
