from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(verbose_name='user_id', primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, default=None, verbose_name=_('Username'))
    first_name = models.CharField(max_length=64, null=False, blank=False, verbose_name=_('First name'))
    last_name = models.CharField(max_length=64, null=True, blank=True, default=None, verbose_name=_('Last name'))
    bio = models.CharField(max_length=70, null=True, blank=True, default=None, verbose_name=_('Bio'))
    phone_number = PhoneNumberField(null=True, blank=True, default=None, verbose_name=_('Phone number'))
    language_code = models.CharField(max_length=3, null=False, blank=False, verbose_name=_('Language code'))
    deep_link = models.CharField(max_length=64, null=True, blank=True)

    is_blocked_bot = models.BooleanField(default=False, verbose_name=_('is blocked bot'))
    is_banned = models.BooleanField(default=False, verbose_name=_('is banned'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def __str__(self):
        full_name = f'{self.first_name}'
        if self.last_name is not None:
            full_name += f' {self.last_name}'
        return full_name
