from django.contrib.auth import get_user_model
from rest_framework import generics

from authentication.serializers import UserSerializer
from utils.views import DestroyAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView

User = get_user_model()


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'middle_name', ]
    filterset_fields = ['is_active', 'is_staff', 'is_deleted', ]


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(CreateAPIView):
    serializer_class = UserSerializer


class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDelete(DestroyAPIView):
    queryset = User.objects.filter(is_deleted=False)

