
Mustache for Pyramid
====================

Implements Mustache templating for Pyramid views.


Installation
------------

Get the source code and install the package:

  git clone git://github.com/BlueDragonX/pyramid_mustache.git
  cd pyramid_mustache
  python setup.py install


Usage
-----

Add the following in main() under the project's __init__.py:

  config.add_renderer('.mustache', 'pyramid_mustache.MustacheRendererFactory')


Authors
-------

The pyramid_mustache is the product of work by the following people:

- Ryan Bourgeois <bluedragonx@gmail.com>

License
-------

The pyramid_mustache project is licensed under the BSD-derived license and is
copyright (c) 2012 Ryan Bourgeois. A copy of the license is included in the
LICENSE file. If it is missing a copy can be found on the [project page][1].

[1]: https://github.com/BlueDragonX/pyramid_mustache/blob/master/LICENSE	License

