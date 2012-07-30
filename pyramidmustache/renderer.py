"""
Define the Pyramid Mustache renderer.
"""

import os
import pystache
from pyramid.path import package_path
from pyramid.asset import resolve_asset_spec


class MustacheRendererFactory(object):

    """Renderer factory for Mustache templates."""

    def __init__(self, info):
        """Initialize the renderer. Saves info for later."""
        self.info = info

    def __call__(self, value, system):
        """Render the template."""
        pkg, name = resolve_asset_spec(self.info.name)
        tpl = os.path.join(package_path(self.info.package), name)
        return pystache.render(open(tpl, 'r').read(), value)

