from django.urls import path

from authentication.views import api_views

urlpatterns = [
    path('login', api_views.login_view),
    path('logout', api_views.logout_view),
]
