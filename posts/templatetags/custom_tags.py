# from .models import YourModel
from django import template
register = template.Library()

# custom template tags used to implement the recursive commenting functionality
@register.simple_tag
def create_stack(stack, takes_context=True):
    array = []
    for item in stack:
        if item.comment:
            pass
        else:
            array.append(item)
    return array

@register.simple_tag
def pop_item_from_stack(stack):
    return stack.pop(0)

@register.simple_tag
def push_item_onto_stack(stack, item):
    stack.insert(0, item)
    # return stack


@register.simple_tag
def add(a, b):
    return a+b


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def subtract(value, arg):
    return value - arg
