from django import template
register = template.Library()


@register.filter
def get_module_name(string):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    split_name = string.split('.')
    return string if len(split_name) < 2 else split_name[1]
