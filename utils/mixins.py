import json

from django.core.exceptions import ValidationError
from rest_framework import exceptions


class APIViewMixin:

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            kwargs = json.loads(self.request.body)
            obj_pk = kwargs['id']
        except json.decoder.JSONDecodeError:
            raise exceptions.ParseError
        try:
            obj = queryset.get(pk=obj_pk)
        except (TypeError, ValueError, ValidationError, queryset.model.DoesNotExist):
            raise exceptions.NotFound
        self.check_object_permissions(self.request, obj)

        return obj
