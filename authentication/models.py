import binascii
import os
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from core import settings
from rest_framework.authtoken.models import Token as AuthToken
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, username, first_name=None, last_name=None, password=None):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, first_name=None, last_name=None):
        user = self.create_user(password=password,
                                username=username,
                                first_name=first_name,
                                last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)

    username = models.CharField(max_length=32, null=False, blank=False, unique=True, verbose_name=_('Username'))
    email = models.EmailField(unique=True, default=None, null=True, blank=True, verbose_name=_('Email'))
    phone_number = PhoneNumberField(null=True, blank=True, default=None, verbose_name=_('Phone number'))
    first_name = models.CharField(max_length=64, null=False, blank=False, verbose_name=_('First name'))
    last_name = models.CharField(max_length=64, null=True, default=None, blank=True, verbose_name=_('Last name'))
    middle_name = models.CharField(max_length=64, null=True, default=None, blank=True, verbose_name=_('Middle name'))
    date_joined = models.DateField(null=True, default=None, blank=True, verbose_name=_('Date joined'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    is_deleted = models.BooleanField(verbose_name=pgettext_lazy('Мужской род', 'deleted'), default=False)
    deleted_at = models.DateTimeField(verbose_name=_('deleted at'), null=True, default=None, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    @property
    def full_name(self):
        full_name = self.first_name
        if self.last_name is not None:
            full_name = self.last_name + ' ' + full_name
        if self.middle_name is not None:
            full_name += ' ' + self.middle_name
        return full_name
    full_name.fget.short_description = _('Full name')


class Token(AuthToken):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    last_use = models.DateTimeField(_("Last use"), auto_now=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super(AuthToken, self).save(force_insert, force_update)
