from django.contrib.auth import get_user_model
from rest_framework import generics

from administration.models import Department, Position
from administration.serializers import DepartmentSerializer, PositionSerializer
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


class DepartmentsList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', ]
    filterset_fields = ['parent_department_id', 'is_active', 'is_deleted', ]


class DepartmentDetail(RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentCreate(generics.CreateAPIView):
    serializer_class = DepartmentSerializer


class DepartmentUpdate(UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDelete(DestroyAPIView):
    queryset = Department.objects.filter(is_deleted=False)


class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    search_fields = ['name', ]
    filterset_fields = ['parent_position_id', 'is_head', 'is_active', 'is_deleted', ]


class PositionDetail(RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionCreate(generics.CreateAPIView):
    serializer_class = PositionSerializer


class PositionUpdate(UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDelete(DestroyAPIView):
    queryset = Position.objects.filter(is_deleted=False)
