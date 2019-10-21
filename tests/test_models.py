from django.core.exceptions import ValidationError
from django.test import TestCase

from tests.app.constants import DRAFT, PUBLISHED, DUMMY, AUTO
from tests.app.models import Post, Category
from tests.factories import PostFactory, CategoryFactory


class ModelTest(TestCase):
    def test_check_allowed_transitions(self):
        post = PostFactory()
        self.assertEqual(DRAFT, post.status)
        exception = None
        try:
            post.status = PUBLISHED
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        self.assertIsNone(exception)

    def test_check_status_change_on_transition(self):
        post = PostFactory()
        self.assertEqual(DRAFT, post.status)
        exception = None
        try:
            post.status = AUTO
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        self.assertIsNone(exception)
        self.assertEqual(AUTO, post.status, "status doesn't change to published")

    def test_check_no_handler_on_transition(self):
        post = PostFactory()
        self.assertEqual(DRAFT, post.status)
        exception = None
        try:
            post.status = DUMMY
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        self.assertIsNone(exception)

    def test_check_forbidden_transitions(self):
        post = PostFactory(status=PUBLISHED)
        self.assertEqual(PUBLISHED, post.status)
        exception = None
        try:
            post.status = DRAFT
            post.save()
        except ValidationError as validation_exception:
            exception = validation_exception
        self.assertIsNotNone(exception)
        self.assertIsInstance(exception, ValidationError)

    def test_search_mixin(self):
        PostFactory.create_batch(size=10)
        PostFactory(title="very exact title")
        posts = Post.objects.search(query="exact")
        self.assertEqual(1, posts.count())

    def test_search_mixin_no_search_fules(self):
        CategoryFactory.create_batch(size=10)
        categories = Category.objects.search(query="foo")
        self.assertEqual(0, categories.count())
