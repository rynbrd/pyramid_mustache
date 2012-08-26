# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
The package entry point.
"""

import os
from pyramid.path import AssetResolver
from pystache.renderer import Renderer
from pyramid_mustache.renderer import MustacheRendererFactory


__all__ = ['MustacheRendererFactory', 'Session', 'session', 'configure']


class Session(object):

    """
    Store session information.
    """

    search_key = 'mustache.search'
    search_default = []

    def __init__(self):
        """Initialize the object."""
        self.configured = False
        self.search = []

    def configure(self, settings):
        """Configure the session. Sets the template search path."""
        self.search = []
        if self.search_key in settings:
            paths = settings[self.search_key].split(',')
        else:
            paths = self.search_default
        [self.add_search_asset(path) for path in paths]
        self.configured = True

    def add_search_asset(self, asset):
        """Add a template search directory to the session."""
        path = os.path.realpath(AssetResolver().resolve(asset).abspath())
        self.search.append(path)

    def get_renderer(self):
        """Generate a renderer using the stored search directories."""
        return Renderer(search_dirs=self.search)


session = Session()


def configure(config):
    """Configure Pyramid to use Mustache."""
    session.configure(config.get_settings())
    config.add_renderer('.mustache',
        'pyramid_mustache.MustacheRendererFactory')

