from django.contrib import admin
from .models import Application, Tag

# Register your models here.
admin.site.register(Application)
admin.site.register(Tag)