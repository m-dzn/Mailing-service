from django.urls import path, include

from . import api_urls, render_urls

urlpatterns = [
    path('api/', include(api_urls.urlpatterns)),
] + render_urls.urlpatterns
