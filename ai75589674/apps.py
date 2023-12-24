from django.apps import AppConfig

class Ai75589674Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai75589674'

    def ready(self):
        import ai75589674.pdf_generator  # Corrected import statement

