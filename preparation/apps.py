# preparation/apps.py

from django.apps import AppConfig

class PreparationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'preparation'

    def ready(self):
        # Import the signals module to register signal handlers
        import preparation.signals