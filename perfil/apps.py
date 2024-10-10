from django.apps import AppConfig


class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfil'

    def ready(self, *args, **kwargs) -> None:
        import perfil.signals
        super_ready = super().ready()
        return super_ready
