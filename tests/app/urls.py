from django.urls import include, path

urlpatterns = [path("api/v1/", include("tests.app.router", namespace="api_v1"))]
