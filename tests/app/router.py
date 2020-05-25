from django.urls import path, include
from rest_framework import routers

from tests.app.resources import BlogViewSet, PostViewSet

app_name = "api_v1"
router = routers.DefaultRouter()
router.register("posts", viewset=PostViewSet)
router.register("blogs", viewset=BlogViewSet)

urlpatterns = [path("", include(router.urls))]
