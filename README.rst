Django Nginx Memcache
=====================
Provides a view decorator. Use it to cache content in Memcache for nginx to
retrieve.

The cache keys are hashed using an md5 of the the request path *without*
GET parameters,

Installation
------------

#. The usual pip or easy_install from `github <https://github.com/pcraciunoiu/django-nginx-memcache>`_::

    pip install -e git://github.com/pcraciunoiu/django-nginx-memcache#egg=django-nginx-memcache

#. Add ``nginx_memcache`` to your installed apps::

    INSTALLED_APPS = (
        # ...
        'nginx_memcache',
        # ...
    )

#. Then enable it and set the default cache timeout::

    CACHE_NGINX = True
    CACHE_NGINX_TIME = 3600 * 24  # 1 day, in seconds
    # Default backend to use from settings.CACHES
    # May need to update the nginx conf if this is changed
    CACHE_NGINX_ALIAS = 'default'

#. Setup Memcached appropriately as described in `Django's cache framework docs <http://docs.djangoproject.com/en/dev/topics/cache/#memcached>`_.

#. Install Nginx with the `set_misc <https://github.com/agentzh/set-misc-nginx-module>`_ or `set_hash module <https://github.com/simpl/ngx_http_set_hash>`_. This is required to compute md5 cache keys from within Nginx.
#. Configure Nginx for direct Memcached page retrieval, i.e::

    location / {
        # Extract cache key args and cache key.
        if ($http_cookie ~* "pv=([^;]+)(?:;|$)") {
          set $page_version $1;
        }
        set_md5 $hash_key $uri&pv=$page_version;
        set $memcached_key :1:$hash_key;

        default_type       text/html;
        memcached_pass     127.0.0.1:11211;
        error_page         404 @cache_miss;
    }

    location @cache_miss {
        # Your previous django config goes here...
    }


Usage
-----

nginx_memcache.decorators.cache_page_nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``cache_page_nginx`` decorator caches the view's response content in Memcache. Any arguments are optional and outlined below.

Example::

    from nginx_memcache.decorators import cache_page_nginx

    @cache_page_nginx
    def my_view(request):
        ...

This will cache the view's response string in Memcache, and hereafter Nginx
will serve from Memcache directly, without hitting your Django server,
until the cache key expires.

Optional parameters
+++++++++++++++++++

``cache_timeout``
  Defaults to ``settings.CACHE_NGINX_TIME`` if not specified.

``page_version_fn``
  Use this to return a stringifiable version of the page, depending on the
  request. Example::

    def get_page_version(request):
        if request.user.is_authenticated():
            return 'authed'
        return 'anonymous'

``anonymous_only``
  Don't cache the page unless the user is anonymous, i.e. not authenticated.

Full List of Settings
~~~~~~~~~~~~~~~~~~~~~

``CACHE_NGINX``
  *Required.* Set this to True to enable the decorator.

``CACHE_NGINX_TIME``
  Default cache timeout.

``CACHE_NGINX_ALIAS``
  Which cache backend to use from `settings.CACHES <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-CACHES>`_

Contributing
============
If you'd like to fix a bug, add a feature, etc

#. Start by opening an issue.
    Be explicit so that project collaborators can understand and reproduce the
    issue, or decide whether the feature falls within the project's goals.
    Code examples can be useful, too.

#. File a pull request.
    You may write a prototype or suggested fix.

#. Check your code for errors, complaints.
    Use `check.py <https://github.com/jbalogh/check>`_

#. Write and run tests.
    Write your own test showing the issue has been resolved, or the feature
    works as intended.

Running Tests
=============
To run the tests::

    python manage.py test nginx_memcache
