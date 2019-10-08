from django.urls import path, include

urlpatterns = [path("api/v1/", include("tests.app.router", namespace="api_v1"))]
