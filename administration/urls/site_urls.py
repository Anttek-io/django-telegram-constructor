from django.urls import path

from administration.views import site_views

urlpatterns = [
    path('', site_views.Index.as_view(), name='index'),

    path('departments/create', site_views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/', site_views.DepartmentListView.as_view(), name='departments_list'),
    path('departments/<int:pk>', site_views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/<int:pk>/delete', site_views.DepartmentDeleteView.as_view(), name='department_delete'),

    path('positions/create', site_views.PositionCreateView.as_view(), name='position_create'),
    path('positions/', site_views.PositionListView.as_view(), name='positions_list'),
    path('positions/<int:pk>', site_views.PositionDetailView.as_view(), name='position_detail'),
    path('positions/<int:pk>/delete', site_views.PositionDeleteView.as_view(), name='position_delete'),
]
