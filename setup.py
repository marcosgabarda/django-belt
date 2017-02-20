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

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


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
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Simple package with some utilities for Django',
    long_description=README,
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    cmdclass={
        'build_static': BuildStaticCommand,
        'build_py': BuildPyCommand,
    }
)
