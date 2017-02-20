# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.test import TestCase

from tests.app.models import Post


class TestBeltModels(TestCase):

    def test_gis_timestamped_attributes(self):
        post = Post()
        self.assertTrue(hasattr(post, "created"))
        self.assertTrue(hasattr(post, "modified"))
