from django import template


register = template.Library()


@register.filter
def getitem(dict_obj: dict, key: str):
    return dict_obj.get(key)


@register.filter
def dotted_string(value: float, after_dot: int = 1) -> str:
    return str(round(value, after_dot)).replace(',', '.')


@register.filter
def split(value: str, sep: str) -> list:
    return value.split(sep)
