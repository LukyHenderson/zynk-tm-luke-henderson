from django.apps import AppConfig

class AppTMConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appTM'

    def ready(self):
        import appTM.signals  # connects to logout signal for signout