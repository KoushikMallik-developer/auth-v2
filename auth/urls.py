from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("api/v2/", include("api.urls"))]
