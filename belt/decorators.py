import os
import shutil


def delete_after(filename):
    """Decorator to be sure the file given by parameter is deleted after the
    execution of the method.
    """

    def delete_after_decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            finally:
                if os.path.isfile(filename):
                    os.remove(filename)
                if os.path.isdir(filename):
                    shutil.rmtree(filename)

        return wrapper

    return delete_after_decorator
