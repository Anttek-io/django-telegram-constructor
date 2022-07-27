from django.urls import path

from administration import views

urlpatterns = [
    path('', views.index_view, name="index"),
]