from collections import namedtuple

from django.contrib.contenttypes.models import ContentType

from logger.models import CustomLogEntry, ADDITION, CHANGE, DELETION, CustomLogEntryChange

FieldChange = namedtuple('FieldChange', ['field_name', 'field_type', 'old_value_str', 'new_value_str'])


def get_content_type_for_model(obj):
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


def log_addition(request, obj):

    cle = CustomLogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=ADDITION,
    )
    return cle


def log_serializer_change(request, obj, serializer):
    changes = []
    for field, value in serializer.validated_data.items():
        field_type = type(obj)._meta.get_field(field).get_internal_type()
        new_value = value
        old_value = getattr(obj, field)
        if new_value == old_value:
            continue
        changes.append(FieldChange(field, field_type, old_value, new_value))
    return log_change(request, obj, changes)


def log_form_change(request, obj, form):
    changes = []
    for field in form.changed_data:
        field_type = type(obj)._meta.get_field(field).get_internal_type()
        new_value = getattr(form.instance, field)
        old_value = getattr(obj, field)
        changes.append(FieldChange(field, field_type, old_value, new_value))
    return log_change(request, obj, changes)


def log_change(request, obj, changes: list = None):
    cle = CustomLogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=CHANGE,
    )
    for change in changes:
        CustomLogEntryChange.objects.create(
            log_entry=cle,
            field_name=change.field_name,
            field_type=change.field_type,
            old_value_str=change.old_value_str,
            new_value_str=change.new_value_str
        )
    return cle


def log_deletion(request, obj):

    cle = CustomLogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=DELETION,
    )
    return cle
