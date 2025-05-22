from django import template
from ..models import Application, Tag, PreviousParticipantEntities

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
    return s.replace("_", " ")


@register.filter(name="get_obj")
def get_obj(field_name):

    if field_name == "Tags":
        field_vals = list(Tag.objects.values_list("name", flat=True).distinct())
    else:
        field_vals = list(Application.objects.values_list(field_name, flat=True).distinct())
    return ['' if v is None else v for v in field_vals]


@register.filter(name="op")
def op(s):

    return f"{s}_op"


@register.filter(name="get_type")
def get_type(datalist):

    return datalist[0]


@register.filter(name="get_default")
def get_default(datalist):

    return datalist[1]


@register.filter(name="ppes")
def ppes(obj):

    if obj:
        try:

            return list(obj.previousparticipantentities_set.all())
        except Exception as e:
            print(e)


@register.filter(name="get_ppe_field")
def get_ppe_field(form, number):

    if form:
        return form[f"ppe{number}"]
