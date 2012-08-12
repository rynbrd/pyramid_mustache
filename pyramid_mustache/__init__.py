# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
The package entry point.
"""

import os
from pyramid.path import package_path
from pystache.renderer import Renderer
from pyramid_mustache.renderer import (MustacheRendererFactory,
    MustacheFieldRenderer)


class Session:

    """
    Store session information.
    """

    templates_key = 'mustache.templates'
    templates_default = ['templates']

    def __init__(self):
        """Initialize the object."""
        self.configured = False
        self.templates = None

    def configure(self, settings):
        """Configure the session. Sets the template search path."""
        if self.templates_key in settings:
            self.templates = settings[self.templates_key].split(':')
        else:
            self.templates = self.templates_default
        self.configured = True

    def get_templates(self, package):
        """
        Generate the list of template search paths relative to the given
        package.
        """
        pkgpath = package_path(package)
        def fixpath(path):
            if not os.path.isabs(path):
                path = os.path.join(pkgpath, path)
            return path
        return [fixpath(p) for p in self.templates]

    def get_renderer(self, package):
        """
        Generate a renderer for a package.
        """
        return Renderer(search_dirs=self.get_templates(package))


session = Session()


def configure(config):
    """Configure Pyramid to use Mustache."""
    session.configure(config.get_settings())
    config.add_renderer('.mustache',
        'pyramid_mustache.MustacheRendererFactory')

