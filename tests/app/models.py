from django.db import models

from belt.models import StatusMixin
from tests.app.constants import STATUS_OPTIONS, DRAFT, PUBLISHED
from tests.app.managers import PostQuerySet, CategoryQuerySet


class Post(StatusMixin, models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_OPTIONS, default=DRAFT)

    objects = PostQuerySet.as_manager()

    SEARCH_FIELDS = ["title", "content"]
    ALLOWED_TRANSITIONS = [(DRAFT, PUBLISHED)]
    FORBIDDEN_TRANSITIONS = [(PUBLISHED, DRAFT)]

    TRANSITION_HANDLERS = {(DRAFT, PUBLISHED): "published"}

    def published(self):
        pass

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Category(models.Model):
    objects = CategoryQuerySet.as_manager()
