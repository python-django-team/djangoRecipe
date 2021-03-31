"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import cache_control

urlpatterns = [
    # main/urls.pyをインポート
    path("", include("app.urls")),
    path("admin/", admin.site.urls),
    # PWA用
    path(
        "sw.js",
        TemplateView.as_view(
            template_name="sw.js", content_type="application/javascript",
        ),
        name="service-worker",
    ),  
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [ re_path(r'^static/(?P<path>.*)$', RedirectView.as_view(url="/random")) ]
