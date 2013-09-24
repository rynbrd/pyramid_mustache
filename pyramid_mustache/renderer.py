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

        pkg_path = package_path(self.info.package)
        tpl_path = os.path.join(pkg_path, name)
        tpl_dir = os.path.split(tpl_path)[0]

        renderer = pystache.Renderer(search_dirs=[tpl_dir, pkg_path])
        return renderer.render_path(tpl_path, value)

