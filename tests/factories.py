from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText

from tests.app.models import Post, Category, Blog
from factory.declarations import SubFactory


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog


class PostFactory(DjangoModelFactory):
    blog = SubFactory(BlogFactory)
    title = FuzzyText()
    content = FuzzyText()

    class Meta:
        model = Post


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
