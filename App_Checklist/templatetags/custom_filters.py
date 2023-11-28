# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='get')
def get_item(dictionary, key):
    return dictionary.get(key)
