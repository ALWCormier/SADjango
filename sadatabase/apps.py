from django.apps import AppConfig


class SadatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sadatabase'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
