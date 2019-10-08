from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText

from tests.app.models import Post, Category


class PostFactory(DjangoModelFactory):
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Post


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
