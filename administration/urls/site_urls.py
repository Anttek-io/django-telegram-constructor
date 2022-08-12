from django.urls import path

from administration.views import site_views

urlpatterns = [
    path('', site_views.Index.as_view(), name='index'),
]
