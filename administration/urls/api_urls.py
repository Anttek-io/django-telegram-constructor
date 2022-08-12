from django.urls import path

from administration.views import api_views

urlpatterns = [
    # Users
    path('users/list', api_views.UsersList.as_view()),
    path('users/detail', api_views.UserDetail.as_view()),
    path('users/create', api_views.UserCreate.as_view()),
    path('users/update', api_views.UserUpdate.as_view()),
    path('users/delete', api_views.UserDelete.as_view()),
]
