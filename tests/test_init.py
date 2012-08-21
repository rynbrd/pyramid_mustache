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
from pyramid_mustache import Session
from pyramid.path import package_path
from pystache.renderer import Renderer
from .dummy import DummyPackage, DummyConfig


class BaseCase(unittest.TestCase):

    """
    Set up test data for the package.
    """

    def setUp(self):
        """Set up the test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        self.search_key = 'mustache.search'
        self.search_default = []
        self.search_custom = ['../tests/templates_custom']
        self.search_resolved = [os.path.realpath(os.path.join(here, path))
            for path in self.search_custom]
        self.settings_default = {}
        self.settings_custom = {
            self.search_key: ','.join(self.search_custom)}
        self.package_name = 'pyramid_mustache'
        self.package = DummyPackage(self.package_name)
        self.package_path = package_path(self.package)


class TestSession(BaseCase):

    """
    Test the session class.
    """

    def test_class(self):
        """Test class attributes."""
        self.assertEqual(Session.search_key,
            self.search_key, 'Session.search_key is invalid')
        self.assertEqual(Session.search_default,
            self.search_default, 'Session.search_default is invalid')

    def test_init(self):
        """Test __init__ method."""
        session = Session()
        self.assertFalse(session.configured,
            'session.configured is invalid')
        self.assertEqual(session.search, self.search_default,
            'session.search is invalid')

    def test_configure_default(self):
        """Test the configure method with default settings."""
        session = Session()
        session.configure(self.settings_default)
        self.assertEqual(session.search, self.search_default,
            'session.search is invalid')
        self.assertTrue(session.configured,
            'session.configured is invalid')

    def test_configure_custom(self):
        """Test the configure method with custom settings."""
        session = Session()
        session.configure(self.settings_custom)
        self.assertEqual(session.search, self.search_resolved,
            'session.search is invalid')
        self.assertTrue(session.configured,
            'session.configured is invalid')

    def test_get_renderer_default(self):
        """Test the get_renderer method."""
        session = Session()
        session.configure(self.settings_default)
        renderer = pyramid_mustache.session.get_renderer()
        self.assertIsInstance(renderer, Renderer, 'renderer class is invalid')
        self.assertEqual(renderer.search_dirs, self.search_default,
            'renderer.search_dirs is invalid')

    def test_get_renderer_default(self):
        """Test the get_renderer method."""
        session = Session()
        session.configure(self.settings_custom)
        renderer = session.get_renderer()
        self.assertIsInstance(renderer, Renderer, 'renderer class is invalid')
        self.assertEqual(renderer.search_dirs, self.search_resolved,
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

