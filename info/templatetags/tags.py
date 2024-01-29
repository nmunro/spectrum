from django import template

register = template.Library()

@register.filter(name="class_name")
def class_name(instance):
    return instance._meta.model.__name__
