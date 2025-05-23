# users/apps.py

from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # Ensure the signals are loaded when the app is ready
