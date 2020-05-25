from django.db import models
from django.utils import timezone

from belt.models import StatusMixin
from belt.models import StatusMixin, LogicDeleteMixin
from tests.app.constants import STATUS_OPTIONS, DRAFT, PUBLISHED, DUMMY, AUTO
from tests.app.managers import PostQuerySet, CategoryQuerySet, BlogQuerySet


class Blog(models.Model):
    objects = BlogQuerySet.as_manager()


class Post(StatusMixin, LogicDeleteMixin, models.Model):
    blog = models.ForeignKey(Blog, related_name="posts", on_delete=models.CASCADE)

    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_OPTIONS, default=DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)

    objects = PostQuerySet.as_manager()

    SEARCH_FIELDS = ["title", "content"]
    ALLOWED_TRANSITIONS = [(DRAFT, PUBLISHED), (DRAFT, AUTO), (DRAFT, DUMMY)]
    FORBIDDEN_TRANSITIONS = [(PUBLISHED, DRAFT)]

    TRANSITION_HANDLERS = {(DRAFT, PUBLISHED): "published", (DRAFT, AUTO): "auto"}

    def pre_logic_delete(self):
        pass

    def post_logic_delete(self):
        pass

    def pre_undo_logic_delete(self):
        pass

    def post_undo_logic_delete(self):
        pass

    def published(self):
        self.published_at = timezone.now()
        self.save()

    def dummy(self):
        pass

    def auto(self):
        self.status = PUBLISHED
        self.save()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Category(models.Model):
    objects = CategoryQuerySet.as_manager()
