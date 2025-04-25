from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'sadatabase'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('detail', views.detail, name='detail'),
    path('edit', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('change_terms', views.change_terms, name="change_terms"),
    path('update_field_defaults', views.update_field_defaults, name="update_field_defaults"),
    path('save_edits', views.save_edits, name="save_edits"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()