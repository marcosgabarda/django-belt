from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny

from belt.rest_framework.mixins import ActionSerializersMixin
from tests.app.filters import PostFilter
from tests.app.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "status"]


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "status"]


class PostViewSet(ActionSerializersMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    filterset_class = PostFilter
    action_serializers = {"retrieve": PostDetailSerializer}
