"""
Package implementing support for Mustache templates in Pyramid.
"""

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(here, 'README.md')

requires = [
    'pyramid>=1.3.0',
    'pystache>=0.5.0']
testing_extras = [
    'nose']

setup(
    name='pyramid_mustache',
    version='0.1',
    description="Implements support for Mustache templates in Pyramid.",
    long_description=open(readme).read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Framework :: Pyramid",
        "License :: OSI Approved :: BSD License"],
    keywords='web wsgi pylons pyramid mustache',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='https://github.com/BlueDragonX/pyramid_mustache',
    license='BSD-derived',
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + testing_extras,
    entry_points="")

