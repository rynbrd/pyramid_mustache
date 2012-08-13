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

