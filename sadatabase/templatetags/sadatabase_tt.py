from django import template
from ..models import Application

register = template.Library()


@register.filter(name="phase_name")
def phase_name(obj):
    name_map = {
        "pre": "Pre-Construction Phase",
        "during": "During Construction Phase",
        "post": "Post-Construction Phase",
        "af": "Additional Funding Phase"
    }
    return name_map[obj]


@register.filter(name="tags")
def tags(obj):
    tags_out = []
    if obj.tag1:
        tags_out.append(obj.tag1)
    if obj.tag2:
        tags_out.append(obj.tag2)
    if obj.tag3:
        tags_out.append(obj.tag3)
    if obj.tag4:
        tags_out.append(obj.tag4)
    return tags_out


@register.filter(name="readable")
def readable(s):
    return s.replace("_", " ").title()


@register.filter(name="get_obj")
def get_obj(field_name):

    field_vals = list(Application.objects.values_list(field_name, flat=True).distinct())
    return field_vals


@register.filter(name="op")
def op(s):

    return f"{s}_op"
