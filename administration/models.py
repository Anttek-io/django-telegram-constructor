from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from core import settings


class Department(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    parent_department = models.ForeignKey('administration.Department', on_delete=models.SET_NULL, null=True,
                                          default=None, blank=True, verbose_name=_('Parent department'),
                                          related_name='child_departments')

    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    is_deleted = models.BooleanField(verbose_name=_('deleted'), default=False)
    deleted_at = models.DateTimeField(verbose_name=_('deleted at'), null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    parent_position = models.ForeignKey('administration.Position', on_delete=models.SET_NULL, null=True, default=None,
                                        blank=True, verbose_name=_('Parent position'), related_name='child_positions')
    is_head = models.BooleanField(verbose_name=_('is head position'), default=False)

    is_active = models.BooleanField(verbose_name=pgettext_lazy('Женский род', 'is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    is_deleted = models.BooleanField(verbose_name=pgettext_lazy('Женский род', 'deleted'), default=False)
    deleted_at = models.DateTimeField(verbose_name=_('deleted at'), null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('position')
        verbose_name_plural = _('positions')

    def __str__(self):
        return self.name


class Employment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'),
                             related_name='employments')
    department = models.ForeignKey('administration.Department', on_delete=models.CASCADE, verbose_name=_('Department'),
                                   related_name='employments')
    position = models.ForeignKey('administration.Position', on_delete=models.CASCADE, verbose_name=_('Position'),
                                 related_name='employments')
    is_head = models.BooleanField(verbose_name=_('is head'), default=False)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name=_('assigned by'),
                                    related_name='employee_assignments')

    is_active = models.BooleanField(verbose_name=pgettext_lazy('средний род', 'is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('employment')
        verbose_name_plural = _('employments')

    def __str__(self):
        return f'{self.user.full_name} - {self.position} {_("in")} {self.department}'
