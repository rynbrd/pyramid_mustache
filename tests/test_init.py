# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the pyramid_mustache module.
"""

import os
import unittest
import pyramid_mustache
from pyramid.path import package_path
from pystache.renderer import Renderer
from .dummy import DummyPackage, DummyConfig


class PackageTestData(unittest.TestCase):

    """
    Set up test data for the package.
    """

    def setUp(self):
        """Set up the test data."""
        self.templates_key = 'mustache.templates'
        self.templates_default = ['templates']
        self.templates_custom = ['templates_custom']
        self.settings_default = {}
        self.settings_custom = {
            self.templates_key: ':'.join(self.templates_custom)}
        self.package_name = 'pyramid_mustache'
        self.package = DummyPackage(self.package_name)
        self.package_path = package_path(self.package)


class TestSession(PackageTestData):

    """
    Test the session class.
    """

    def reset(self):
        pyramid_mustache.session = pyramid_mustache.Session()

    def test_class(self):
        """Test class attributes."""
        self.assertEqual(pyramid_mustache.Session.templates_key,
            self.templates_key, 'Session.templates_key is invalid')
        self.assertEqual(pyramid_mustache.Session.templates_default,
            self.templates_default, 'Session.templates_default is invalid')

    def test_init(self):
        """Test __init__ method."""
        self.reset()
        self.assertFalse(pyramid_mustache.session.configured,
            'session.configured is invalid')
        self.assertTrue(pyramid_mustache.session.templates is None,
            'session.templates is invalid')

    def test_configure_default(self):
        """Test the configure method with default settings."""
        self.reset()
        pyramid_mustache.session.configure(self.settings_default)
        self.assertEqual(pyramid_mustache.session.templates,
            self.templates_default, 'session.templates is invalid')
        self.assertTrue(pyramid_mustache.session.configured,
            'session.configured is invalid')

    def test_configure_custom(self):
        """Test the configure method with custom settings."""
        self.reset()
        pyramid_mustache.session.configure(self.settings_custom)
        self.assertEqual(pyramid_mustache.session.templates,
            self.templates_custom, 'session.templates is invalid')
        self.assertTrue(pyramid_mustache.session.configured,
            'session.configured is invalid')

    def test_get_templates_default(self):
        """Test the get_templates method with default settings."""
        template_path = os.path.join(self.package_path,
            self.templates_default[0])
        self.reset()
        pyramid_mustache.session.configure(self.settings_default)
        self.assertEqual(pyramid_mustache.session.get_templates(self.package),
            [template_path], 'session.get_templates is invalid')

    def test_get_templates_custom(self):
        """Test the get_templates method with custom settings."""
        template_path = os.path.join(self.package_path,
            self.templates_custom[0])
        pyramid_mustache.session.configure(self.settings_custom)
        self.assertEqual(pyramid_mustache.session.get_templates(self.package),
            [template_path], 'session.get_templates is invalid')

    def test_get_renderer(self):
        """Test the get_renderer method."""
        template_path = os.path.join(self.package_path,
            self.templates_default[0])
        self.reset()
        pyramid_mustache.session.configure(self.settings_default)
        renderer = pyramid_mustache.session.get_renderer(self.package)
        self.assertIsInstance(renderer, Renderer, 'renderer class is invalid')
        self.assertEqual(renderer.search_dirs, [template_path],
            'renderer.search_dirs is invalid')


class TestModuleFunctions(unittest.TestCase):

    """Test module functions."""

    def test_configure(self):
        """Test the configure function."""
        pyramid_mustache.session = pyramid_mustache.Session()
        config = DummyConfig()
        pyramid_mustache.configure(config)
        self.assertTrue(pyramid_mustache.session.configured,
            'session.configured is invalid')
        self.assertTrue(config.has_renderer('.mustache',
            'pyramid_mustache.MustacheRendererFactory'),
            'renderer not found in config')

