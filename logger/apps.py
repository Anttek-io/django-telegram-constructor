from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logger'
    verbose_name = _('Logging')
