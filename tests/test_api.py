from test_plus import APITestCase

from tests.app.constants import DRAFT, PUBLISHED
from tests.factories import BlogFactory, PostFactory


class PostAPITestCase(APITestCase):
    def test_list_serializer(self):
        PostFactory.create_batch(size=10)
        self.get("api_v1:post-list")
        self.response_200()
        data = self.last_response.json()
        self.assertEqual(10, len(data))
        self.assertNotIn("content", data[0])

    def test_retrieve_serializer(self):
        posts = PostFactory.create_batch(size=10)
        self.get("api_v1:post-detail", pk=posts[0].pk)
        self.response_200()
        data = self.last_response.json()
        self.assertIn("content", data)

    def test_search(self):
        PostFactory.create_batch(title="foo", content="dummy", size=10)
        PostFactory(title="potato")
        self.get("api_v1:post-list", data={"search": "potato"})
        self.response_200()
        data = self.last_response.json()
        self.assertEqual(1, len(data))

    def test_update_status(self):
        post = PostFactory(title="potato", status=DRAFT)
        self.patch("api_v1:post-detail", pk=post.pk, data={"status": PUBLISHED})
        self.response_200()
        post.refresh_from_db()
        self.assertEqual(PUBLISHED, post.status)


class BlogAPITestCase(APITestCase):
    def test_list_serializer(self):
        BlogFactory.create_batch(size=10)
        self.get("api_v1:blog-list")
        self.response_200()
        data = self.last_response.json()
        self.assertEqual(10, len(data))
        self.assertNotIn("content", data[0])

    def test_annotate_total_posts(self):
        blog = BlogFactory()
        PostFactory.create_batch(blog=blog, size=10)
        self.get("api_v1:blog-detail", pk=blog.pk)
        self.response_200()
        self.assertEqual(10, self.last_response.data["total_posts"])
