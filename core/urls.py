"""dtc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from authentication.urls import api_urls as auth_api_urls, site_urls as auth_site_urls
from administration.urls import api_urls as adm_api_urls, site_urls as adm_site_urls

from core import settings

urlpatterns = [
    path('', include((adm_site_urls, 'administration'), namespace='administration')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('auth/', include((auth_site_urls, 'authentication'), namespace='authentication')),

    path('api/adm/', include(adm_api_urls)),
    path('api/auth/', include(auth_api_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
