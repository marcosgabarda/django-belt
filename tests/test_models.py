from django.core.exceptions import ValidationError
import pytest

from tests.app.constants import AUTO, DRAFT, DUMMY, PUBLISHED
from tests.app.models import Blog, Category, Post
from tests.factories import BlogFactory, CategoryFactory, PostFactory


@pytest.mark.django_db
class TestModel:
    def test_check_allowed_transitions(self):
        post: Post = PostFactory()
        assert post.status == DRAFT
        exception = None
        try:
            post.status = PUBLISHED
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        assert exception is None

    def test_check_status_change_on_transition(self):
        post = PostFactory()
        assert post.status == DRAFT
        exception = None
        try:
            post.status = AUTO
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        assert exception is None
        assert post.status == AUTO, "status doesn't change to published"

    def test_check_no_handler_on_transition(self):
        post = PostFactory()
        assert post.status == DRAFT
        exception = None
        try:
            post.status = DUMMY
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        assert exception is None

    def test_check_forbidden_transitions(self):
        post: Post = PostFactory(status=PUBLISHED)
        assert post.status == PUBLISHED
        exception = None
        try:
            post.status = DRAFT
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        assert exception is not None
        assert isinstance(exception, ValidationError)

    def test_search_mixin(self):
        PostFactory.create_batch(size=10)
        PostFactory(title="very exact title")
        posts = Post.objects.search(query="exact")
        assert posts.count() == 1

    def test_search_combined(self):
        PostFactory.create_batch(size=10)
        PostFactory(title="title and", content="content")
        posts = Post.objects.search(query="and content")
        assert posts.count() == 1

    def test_search_mixin_no_search_fules(self):
        CategoryFactory.create_batch(size=10)
        categories = Category.objects.search(query="foo")
        assert categories.count() == 0

    def test_logic_delete(self):
        post: Post = PostFactory()
        post.logic_delete()
        assert post.deleted
        assert post.date_deleted is not None

    def test_undo_logic_delete(self):
        post: Post = PostFactory()
        post.logic_delete()
        assert post.deleted
        post.undo_logic_delete()
        assert not post.deleted
        assert post.date_deleted is None

    def test_annotate_total_posts(self):
        blog = BlogFactory()
        PostFactory.create_batch(blog=blog, size=10)
        annotated_blog = Blog.objects.annotate_total_posts().first()
        assert annotated_blog.total_posts == 10
