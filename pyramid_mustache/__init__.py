"""
Add to the app:

    config.include('pyramid_mustache')

Add your own renderer extension:

    config.add_renderer('.mch', 'pyramid_mustache.MustacheRendererFactory')
"""

from pyramid_mustache.renderer import MustacheRendererFactory


def includeme(config):
    config.add_renderer(".mustache", MustacheRendererFactory)
