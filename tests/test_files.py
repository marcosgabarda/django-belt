import os

from django.test import TestCase

from belt.files import UploadToDir


class TestBeltFilesModule(TestCase):
    def test_upload_to_dir(self):
        destiny_path = "vault"
        file_name = "test_file.jpg"
        upload_to_dir = UploadToDir(destiny_path)
        path = upload_to_dir(None, file_name)
        self.assertEqual(path, os.path.join(destiny_path, file_name))

    def test_upload_to_dir_random_name(self):
        destiny_path = "vault"
        file_name = "test_file.jpg"
        upload_to_dir = UploadToDir(destiny_path, random_name=True)
        path = upload_to_dir(None, file_name)
        self.assertNotEqual(path, os.path.join(destiny_path, file_name))

    def test_upload_to_dir_populate(self):
        class Obj(object):
            title = "foo"

        destiny_path = "vault"
        file_name = "test_file.jpg"
        ext = file_name.split(".")[-1]
        upload_to_dir = UploadToDir(destiny_path, populate_from="title")
        path = upload_to_dir(Obj(), file_name)
        self.assertEqual(path, os.path.join(destiny_path, "%s.%s" % (Obj.title, ext)))
