from django.shortcuts import render

from administration.utils import _get_app_list


def index_view(request):
    app_list = _get_app_list(request)
    return render(request, 'administration/index.html', context={'app_list': app_list})

