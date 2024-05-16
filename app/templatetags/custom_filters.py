from django import template

register = template.Library()


@register.filter
def filesizeformat(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return 'Invalid size'

    if value < 1024:
        return f'{value} bytes'
    elif value < 1024 ** 2:
        return f'{value / 1024:.2f} KB'
    elif value < 1024 ** 3:
        return f'{value / 1024 ** 2:.2f} MB'
    else:
        return f'{value / 1024 ** 3:.2f} GB'


@register.filter
def addstr(value, arg):
    return f'{value}{arg}'
