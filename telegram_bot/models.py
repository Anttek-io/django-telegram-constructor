from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(verbose_name='user_id', primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, default=None, verbose_name=_('Username'))
    first_name = models.CharField(max_length=64, null=False, blank=False, verbose_name=_('First name'))
    last_name = models.CharField(max_length=64, null=True, blank=True, default=None, verbose_name=_('Last name'))
    bio = models.CharField(max_length=70, null=True, blank=True, default=None, verbose_name=_('Bio'))
    phone_number = PhoneNumberField(null=True, blank=True, default=None, verbose_name=_('Phone number'))

    class Meta:
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')

    def __str__(self):
        full_name = f'{self.first_name}'
        if self.last_name is not None:
            full_name += f' {self.last_name}'
        return full_name
