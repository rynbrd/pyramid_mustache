"""
Test the MustacheRendererFactory class.
"""

import os
from unittest import TestCase
from pyramid import testing

class DummyPackage:

    """A dummy package object to pass to the renderer."""

    def __init__(self, name):
        """Initialize the package object with a name."""
        self.__name__ = name


class DummyInfo:

    """A dummy info object to pass to the renderer."""

    def __init__(self, kw):
        """Initialize the info object with some data."""
        self.__dict__.update(kw)
        if 'registry' in self.__dict__:
            self.settings = self.registry.settings


class TestRenderer(TestCase):

    """Perform tests on the MustacheRendererFactory class."""

    def setUp(self):
        """Set up the test case."""
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.request.registry = self.config.registry
        here = os.path.abspath(os.path.dirname(__file__))
        self.templatepath = os.path.join(here, 'templates')
        self.package = DummyPackage('pyramidmustache')
        self.info = DummyInfo({'name': '../tests/templates/test.mustache',
            'package': self.package,
            'registry': self.config.registry})

    def tearDown(self):
        """Tear down the test case."""
        testing.tearDown()
        del self.config

    def test_import(self):
        """Test importing the renderer class."""
        try:
            from pyramidmustache import MustacheRendererFactory
        except ImportError:
            self.assertFalse(True, "failed to import MustacheRendererFactory")

    def test_init(self):
        """Test initializing the renderer object."""
        from pyramidmustache import MustacheRendererFactory
        obj = MustacheRendererFactory(self.info)
        self.assertEqual(obj.info, self.info,
            "failed to initialize MustacheRendererFactory object")

    def test_call(self):
        """Test calling the renderer object."""
        data = {'renderer': 'Mustache'}
        output = "This is a test of the %s renderer.\n" % data['renderer']
        from pyramidmustache import MustacheRendererFactory
        obj = MustacheRendererFactory(self.info)
        self.assertEqual(obj(data, {}), output,
            "failed to render template with MustacheRendererFactory")

