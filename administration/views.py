from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from administration.utils import _get_app_list
from authentication.utils import ExpiringTokenAuthentication


@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# @authentication_classes([ExpiringTokenAuthentication])
def index_view(request):
    app_list = _get_app_list(request)
    return render(request, 'administration/index.html', context={'app_list': app_list})

