from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core import settings


ADDITION = 1
CHANGE = 2
DELETION = 3

ACTION_FLAG_CHOICES = (
    (ADDITION, _("Addition")),
    (CHANGE, _("Change")),
    (DELETION, _("Deletion")),
)


class MyLogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(
        self,
        user_id,
        content_type_id,
        object_id,
        object_repr,
        action_flag,
    ):
        return self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=str(object_id),
            object_repr=object_repr[:200],
            action_flag=action_flag,
        )


class CustomLogEntry(models.Model):
    action_time = models.DateTimeField(_("action time"), default=timezone.now, editable=False, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_("user"), )
    content_type = models.ForeignKey(ContentType, models.SET_NULL, verbose_name=_("content type"),
                                     blank=True, null=True, )
    object_id = models.TextField(_("object id"), blank=True, null=True)
    object_repr = models.CharField(_("object repr"), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_("action flag"), choices=ACTION_FLAG_CHOICES)

    parent = models.ForeignKey('logger.CustomLogEntry', models.CASCADE, 'children', null=True, blank=True, default=None)

    objects = MyLogEntryManager()

    class Meta:
        verbose_name = _("log entry")
        verbose_name_plural = _("log entries")
        ordering = ["-action_time"]

    def __repr__(self):
        return str(self.action_time)

    def __str__(self):
        if self.is_addition():
            return _("Added “%(object)s”.") % {"object": self.object_repr}
        elif self.is_change():
            return _("Changed “%(object)s”") % {
                "object": self.object_repr,
            }
        elif self.is_deletion():
            return _("Deleted “%(object)s.”") % {"object": self.object_repr}

        return _("LogEntry Object")

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION

    def get_edited_object(self):
        """Return the edited object represented by this log entry."""
        return self.content_type.get_object_for_this_type(pk=self.object_id)


class CustomLogEntryChange(models.Model):
    log_entry = models.ForeignKey('logger.CustomLogEntry', models.CASCADE, 'changes', )
    field_name = models.CharField(max_length=128)
    field_type = models.CharField(max_length=32)
    old_value_str = models.TextField(null=True, default='', blank=True)
    new_value_str = models.TextField(null=True, default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('changed field')
        verbose_name_plural = _('changed fields')

    def __str__(self):
        return f'{self.field_name}: {self.old_value_str} -> {self.new_value_str}'


