from django import template

register = template.Library()

@register.filter
def get_by_key(value: dict, key):
    '''фильтр для получения значения атрибута по ключу'''
    return value.get(key, '')


@register.filter
def split_paragraphs(value: str):
    '''фильтр для разбиения описания товара на абзацы'''
    paragraphs = value.split('\n')
    return paragraphs