from django import template


register = template.Library()


@register.filter
def getitem(dict_obj: dict, key: str):
    return dict_obj.get(key)


@register.filter
def round(value: float) -> int:
    return int(value)


@register.filter
def split(value: str, sep: str) -> list:
    return value.split(sep)
