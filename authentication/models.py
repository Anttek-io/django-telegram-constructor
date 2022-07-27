import binascii
import os
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from core import settings
from rest_framework.authtoken.models import Token as AuthToken


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

    username = models.CharField(max_length=24, null=False, blank=False, unique=True)
    email = models.EmailField(unique=True, default=None, null=True)
    first_name = models.CharField(max_length=32, null=True, default=None)
    last_name = models.CharField(max_length=32, null=True, default=None)
    date_joined = models.DateField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
    #
    # def _user_has_module_perms(self, app_label):
    #     """
    #     A backend can raise `PermissionDenied` to short-circuit permission checking.
    #     """
    #     for backend in auth.get_backends():
    #         if not hasattr(backend, "has_module_perms"):
    #             continue
    #         try:
    #             if backend.has_module_perms(self, app_label):
    #                 return True
    #         except PermissionDenied:
    #             return False
    #     return False
    #
    # def has_module_perms(self, app_label):
    #     """
    #     Return True if the user has any permissions in the given app label.
    #     Use similar logic as has_perm(), above.
    #     """
    #     # Active superusers have all permissions.
    #     print(self, app_label)
    #     if self.is_active and self.is_superuser:
    #         return True
    #
    #     return self._user_has_module_perms(self, app_label)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'


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
