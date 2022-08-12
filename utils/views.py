from django.utils import timezone
from rest_framework import generics

from logger.utils import log_deletion, log_serializer_change, log_addition
from utils.mixins import APIViewMixin


class RetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        lookup_param = request.GET.get(self.lookup_field, None)
        if lookup_param:
            kwargs['id'] = lookup_param
        return super(RetrieveAPIView, self).dispatch(request, *args, **kwargs)


class CreateAPIView(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save()
        log_addition(self.request, serializer.instance)


class UpdateAPIView(APIViewMixin, generics.UpdateAPIView):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        log_serializer_change(self.request, self.get_object(), serializer=serializer)
        serializer.save()


class DestroyAPIView(APIViewMixin, generics.DestroyAPIView):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save()
        log_deletion(self.request, instance)
