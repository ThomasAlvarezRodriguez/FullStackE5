from django.apps import AppConfig


class AppChecklistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Checklist'

class UsersConfig(AppConfig):
    name = 'App_Checklist'

    def ready(self):
        import App_Checklist.signals  