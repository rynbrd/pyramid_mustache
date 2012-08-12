"""
Test the MustacheRendererFactory class.
"""

import os
import unittest
import pyramid_mustache
from pyramid import testing
from pystache.renderer import Renderer
from pyramid_mustache.renderer import (MustacheRendererFactory,
    MustacheFieldRenderer)
from formalchemy import FieldSet, Field
from .dummy import DummyPackage, DummyConfig, DummyInfo, DummyModel


class BaseCase(unittest.TestCase):

    """
    Base test case.
    """

    def setUp(self):
        """Set up the test data."""
        here = os.path.abspath(os.path.dirname(__file__))
        self.settings = {
            'mustache.templates': os.path.join(here, 'templates')}
        self.package_name = 'pyramid_mustache'
        self.package = DummyPackage(self.package_name)


class TestRenderer(BaseCase):

    """
    Test the MustacheRendererFactory class.
    """

    def setUp(self):
        """Set up the test data."""
        BaseCase.setUp(self)
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.config.registry.settings = self.settings
        self.request.registry = self.config.registry
        
        self.template_simple = 'simple'
        self.info_simple = DummyInfo({
            'name': self.template_simple + '.mustache',
            'package': self.package,
            'registry': self.config.registry})

        self.template_partial = 'partial_parent'
        self.info_partial = DummyInfo({
            'name': self.template_partial + '.mustache',
            'package': self.package,
            'registry': self.config.registry})

    def reset(self):
        """Reset the session."""
        pyramid_mustache.session = pyramid_mustache.Session()

    def test_init(self):
        """Test initializing the renderer object."""
        pyramid_mustache.session.configure(self.settings)
        factory = MustacheRendererFactory(self.info_simple)
        renderer = pyramid_mustache.session.get_renderer(self.package)
        self.assertEqual(factory.renderer.search_dirs, renderer.search_dirs,
            'factory.renderer is invalid')
        self.assertEqual(factory.template, self.template_simple,
            'factory.template is invalid')

    def test_call_simple(self):
        """Test rendering a simple template."""
        pyramid_mustache.session.configure(self.settings)
        data = {'renderer': 'Mustache'}
        expected = "Rendered by %s.\n" % data['renderer']
        factory = MustacheRendererFactory(self.info_simple)
        self.assertEqual(factory(data, None), expected,
            'failed to render simple template')

    def test_call_partial(self):
        """Test rendering a template with partials."""
        pyramid_mustache.session.configure(self.settings)
        data = {}
        expected = "Include a partial.\nThis is a partial.\n"
        factory = MustacheRendererFactory(self.info_partial)
        self.assertEqual(factory(data, None), expected,
            'failed to render template with partials')


class TestMustacheFieldRenderer(BaseCase):

    """
    Test the MustacheFieldRenderer class.
    """

    def setUp(self):
        """Set up the test data."""
        BaseCase.setUp(self)
        self.value = 'myvalue'
        self.extra = 'myextra'

        self.doc = DummyModel(text=self.value)
        self.fieldset = FieldSet(DummyModel).bind(self.doc)
        self.field = self.fieldset.text

        self.template_nopackage = 'field'
        self.template_package = '%s:%s.mustache' % (self.package_name,
            self.template_nopackage)
        self.output = "Name: %s-%s-%s\nValue: %s\nExtra: %s\n" % (
            type(self.doc).__name__, self.doc.text, 'text', self.doc.text, self.extra)

    def test_init(self):
        """Test the __init__ method."""
        pyramid_mustache.session.configure(self.settings)
        renderer = MustacheFieldRenderer(self.field, self.template_nopackage)
        self.assertIsInstance(renderer.renderer, Renderer,
            'renderer.renderer is invalid')
        self.assertEqual(renderer.template, self.template_nopackage,
            'renderer.template is invalid')

    def test_render_without_package(self):
        """Test the render method without a package."""
        pyramid_mustache.session.configure(self.settings)
        renderer = MustacheFieldRenderer(self.field, self.template_package)
        output = renderer.render(extra=self.extra)
        self.assertEqual(output, self.output,
            'renderer.render method is invalid')

    def test_render_with_custom(self):
        """Test the render method with a package."""
        pyramid_mustache.session.configure(self.settings)
        renderer = MustacheFieldRenderer(self.field, self.template_nopackage)
        output = renderer.render(extra=self.extra)
        self.assertEqual(output, self.output,
            'renderer.render method is invalid')

    def test_factory(self):
        pyramid_mustache.session.configure(self.settings)
        renderer_class = MustacheFieldRenderer.factory(self.template_nopackage)
        renderer = renderer_class(self.field)
        output = renderer.render(extra=self.extra)
        self.assertEqual(output, self.output,
            'MustacheFieldRenderer.factory method is invalid')

