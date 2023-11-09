from django import template

# Create your views here.

register = template.Library()
# template operations


@register.filter(name="mul")
def mul(value, arg):
    return value*arg


@register.simple_tag
def url_replace(request, field, value):
    d = request.GET.copy()
    d[field] = value
    return d.urlencode()


@register.simple_tag
def url_delete(request, field):
    d = request.GET.copy()
    del d[field]
    return d.urlencode()