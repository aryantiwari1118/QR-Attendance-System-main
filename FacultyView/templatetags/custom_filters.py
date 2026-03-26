from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get an item from dictionary using a key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0
