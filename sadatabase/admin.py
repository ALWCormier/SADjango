from django.contrib import admin
from .models import Application, Tag, Event, PreviousParticipantEntities

# Register your models here.
admin.site.register(Application)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(PreviousParticipantEntities)