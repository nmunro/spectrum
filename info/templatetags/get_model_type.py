from django import template

register = template.Library()

@register.filter(name="get_model_type")
def get_model_type(obj):
    print("Got here")
    return obj.__class__.__name__
