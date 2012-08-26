# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Define some dummy objects.
"""

class DummyPackage(object):

    """
    Dummy Pyramid package class.
    """

    def __init__(self, name):
        """Initialize the package object with a name."""
        self.__name__ = name


class DummyConfig(object):

    """
    Dummy Pyramid config class.
    """

    def __init__(self, settings=None):
        """Initialize dummy config data."""
        if settings is None:
            settings = {}
        self.settings = settings
        self.renderers = []

    def get_settings(self):
        """Get the config settings."""
        return self.settings

    def add_renderer(self, name, renderer):
        """Add a renderer to the config."""
        self.renderers.append((name, renderer))

    def has_renderer(self, name, renderer):
        """Check if a renderer exists."""
        renderers = [r for r in self.renderers
            if r[0] == name and r[1] == renderer]
        return len(renderers) > 0


class DummyInfo(object):

    """
    Dummy pyramid info object.
    """

    def __init__(self, kw):
        """Initialize the info object with some data."""
        self.__dict__.update(kw)
        if 'registry' in self.__dict__:
            self.settings = self.registry.settings

