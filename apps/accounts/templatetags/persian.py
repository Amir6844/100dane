from django import template

register = template.Library()

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
EN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

@register.filter
def fa_digits(value):
    if value is None:
        return ''
    return str(value).translate(PERSIAN_DIGITS)

@register.filter
def en_digits(value):
    if value is None:
        return ''
    return str(value).translate(EN_DIGITS)

@register.filter
def avg_color(value):
    try:
        v = float(value)
    except:
        return '#9CA3AF'
    if v >= 17:
        return '#3E9B4F'
    if v >= 12:
        return '#E8B54A'
    return '#C22A4E'

@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None
