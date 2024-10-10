from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'

    def ready(self, *args, **kwargs) -> None:
        import eventos.signals
        super_ready = super().ready()
        return super_ready
