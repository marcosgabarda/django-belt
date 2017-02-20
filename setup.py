# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import os
import subprocess
from distutils.log import INFO

import setuptools
from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')) as history:
    HISTORY = history.read().replace('.. :changelog:', '')

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on belt.VERSION.
version = __import__('belt').get_version()


class BuildStaticCommand(setuptools.Command):
    """A custom command to run npm build command for static files."""

    description = 'run npm run build to compile static files of the package'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        command = ['npm', 'run', 'build']
        self.announce(
            'Running command: %s' % str(command),
            level=INFO)
        subprocess.check_call(command)


class BuildPyCommand(build_py):
    """Custom build command."""

    def run(self):
        self.run_command('build_static')
        setuptools.command.build_py.build_py.run(self)


setup(
    name='django-belt',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Simple package with some utilities for Django',
    long_description=README + '\n\n' + HISTORY,
    url='https://github.com/marcosgabarda/django-belt',
    author='Marcos Gabarda',
    author_email='hey@marcosgabarda.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=1.5',
        'django-model-utils>=2.0',
    ],
    cmdclass={
        'build_static': BuildStaticCommand,
        'build_py': BuildPyCommand,
    }
)
