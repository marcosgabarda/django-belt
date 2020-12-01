from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from belt.rest_framework.mixins import ActionSerializersMixin
from belt.rest_framework.serializers import AnnotatedField
from tests.app.filters import PostFilter
from tests.app.models import Blog, Post


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


class BlogSerializer(serializers.ModelSerializer):
    total_posts = AnnotatedField(default_value=0)

    class Meta:
        model = Blog
        fields = ["id", "total_posts"]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.annotate_total_posts().all()
    serializer_class = BlogSerializer
    permission_classes = (AllowAny,)
