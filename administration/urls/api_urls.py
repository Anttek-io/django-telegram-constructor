from django.urls import path

from administration.views import api_views

urlpatterns = [
    # Users
    path('users/list', api_views.UsersList.as_view()),
    path('users/detail', api_views.UserDetail.as_view()),
    path('users/create', api_views.UserCreate.as_view()),
    path('users/update', api_views.UserUpdate.as_view()),
    path('users/delete', api_views.UserDelete.as_view()),
    # Departments
    path('departments/list', api_views.DepartmentsList.as_view()),
    path('departments/detail', api_views.DepartmentDetail.as_view()),
    path('departments/create', api_views.DepartmentCreate.as_view()),
    path('departments/update', api_views.DepartmentUpdate.as_view()),
    path('departments/delete', api_views.DepartmentDelete.as_view()),
    # Positions
    path('positions/list', api_views.PositionList.as_view()),
    path('positions/detail', api_views.PositionDetail.as_view()),
    path('positions/create', api_views.PositionCreate.as_view()),
    path('positions/update', api_views.PositionUpdate.as_view()),
    path('positions/delete', api_views.PositionDelete.as_view()),
    # Employments

]
