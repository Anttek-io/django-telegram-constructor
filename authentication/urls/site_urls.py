from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import site_views

urlpatterns = [
    path('login/', site_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/auth/login'), name='logout'),

    path('users/', site_views.CustomUserListView.as_view(), name='users_list'),
    path('users/create', site_views.CustomUserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>', site_views.CustomUserDetailView.as_view(), name='user_detail'),
]
