# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.contrib.gis.db import models

from belt.models import GisTimeStampedModel


class Post(GisTimeStampedModel):
    title = models.CharField(max_length=250)
    content = models.TextField()
