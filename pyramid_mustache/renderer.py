# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Define the Pyramid Mustache renderer factory.
"""

import os
import sys
import pyramid_mustache
from pyramid.path import package_of, package_path
from pyramid.asset import resolve_asset_spec
from formalchemy.fields import FieldRenderer


def get_package(module):
    """Return the package that is the parent of module."""
    if not isinstance(module, basestring):
        module = module.__name__
    name = module.split('.')[0]
    __import__(name)
    return sys.modules[name]


class MustacheRendererFactory:

    """
    Renderer factory for Mustache templates.
    """

    def __init__(self, info):
        """Initialize the renderer factory."""
        package, name = resolve_asset_spec(info.name)
        self.renderer = pyramid_mustache.session.get_renderer(
            get_package(info.package))
        self.template = name.rsplit('.', 2)[0]

    def __call__(self, value, system):
        """Render the template."""
        contents = self.renderer.load_template(self.template)
        return self.renderer.render(contents, value)


class MustacheFieldRenderer(FieldRenderer):

    """
    Renderer a FormAlchemy field using a mustache template.
    """

    def __init__(self, field, template):
        """
        Initialie the field renderer.

        :param field: The field to render.
        :param template: A Pyramid asset representing the Mustache template to
            use when rendering the field.
        """
        FieldRenderer.__init__(self, field)
        package, name = resolve_asset_spec(template)
        self.renderer = pyramid_mustache.session.get_renderer(
            get_package(package))
        self.template = name.rsplit('.', 2)[0]

    def render(self, **kwargs):
        """Render the field."""
        kwargs.update({
            'name': self.name,
            'value': self.value})
        content = self.renderer.load_template(self.template)
        return self.renderer.render(content, kwargs)

    @classmethod
    def factory(cls, template):
        """Create a field renderer that uses the given template."""
        class MustacheMetaFieldRenderer(MustacheFieldRenderer):
            """
            Renderer a FormAlchemy field using a mustache template.
            """
            def __init__(self, field):
                """Initialize the field renderer."""
                MustacheFieldRenderer.__init__(self, field, template)
        return MustacheMetaFieldRenderer

