from django.urls import include, path

from core.urls import api_urls, render_urls

urlpatterns = [
    path("api/", include(api_urls.urlpatterns)),
] + render_urls.urlpatterns
