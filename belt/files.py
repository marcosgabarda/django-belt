import hashlib
import os
import random
import time

from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


@deconstructible
class UploadToDir(object):
    """Generates a function to give  to ``upload_to`` parameter in
    models.Fields, that generates an name for uploaded files based on ``populate_from``
    attribute.
    """

    def __init__(self, path, populate_from=None, prefix=None, random_name=False):
        self.path = path
        self.populate_from = populate_from
        self.random_name = random_name
        self.prefix = prefix

    def __call__(self, instance, filename):
        """Generates an name for an uploaded file."""
        if self.populate_from is not None and not hasattr(instance, self.populate_from):
            raise AttributeError(
                "Instance hasn't {} attribute".format(self.populate_from)
            )
        ext = filename.split(".")[-1]
        readable_name = slugify(filename.split(".")[0])
        if self.populate_from:
            readable_name = slugify(getattr(instance, self.populate_from))
        if self.random_name:
            random_name = hashlib.sha256(
                "{}--{}".format(time.time(), random.random()).encode("utf-8")
            )
            readable_name = random_name.hexdigest()
        elif self.prefix is not None:
            readable_name = f"{self.prefix}{readable_name}"
        file_name = "{}.{}".format(readable_name, ext)
        return os.path.join(self.path, file_name)
