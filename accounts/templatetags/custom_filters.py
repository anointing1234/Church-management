from django import template

register = template.Library()

@register.filter
def replace_underscore(value):
    if not isinstance(value, str):
        return value
    return value.replace('_', ' ')
