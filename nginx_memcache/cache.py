import hashlib

from django.conf import settings
from django.core.cache import get_cache


CACHE_NGINX_DEFAULT_COOKIE = 'pv'
CACHE_TIME = getattr(settings, 'CACHE_NGINX_TIME', 3600 * 24)
CACHE_ALIAS = getattr(settings, 'CACHE_NGINX_ALIAS', 'default')
nginx_cache = get_cache(CACHE_ALIAS)


def cache_response(request, response,
                    cache_timeout=CACHE_TIME,
                    cookie_name=CACHE_NGINX_DEFAULT_COOKIE,
                    page_version_fn=None):
    """Cache this response for the web server to grab next time."""
    # get page version
    if page_version_fn:
        pv = page_version_fn(request)
    else:
        pv = ''
    cache_key = get_cache_key(request.get_full_path(), page_version=pv,
                            cookie_name=cookie_name)
    nginx_cache.set(cache_key, response._get_content(), cache_timeout)
    # Store the version, if any specified.
    if pv:
        response.set_cookie(cookie_name, pv)


def get_cache_key(request_path, page_version='',
        cookie_name=CACHE_NGINX_DEFAULT_COOKIE):
    """Use the request path and page version to get cache key."""
    raw_key = u'%s&%s=%s' % (request_path, cookie_name, page_version)
    return hashlib.md5(raw_key).hexdigest()


def invalidate_from_request(request, page_version='',
        cookie_name=CACHE_NGINX_DEFAULT_COOKIE):
    """Delete cache key for this request and page version."""
    invalidate(request.get_full_path(), page_version, cookie_name=cookie_name)


def invalidate(request_path, page_version='',
        cookie_name=CACHE_NGINX_DEFAULT_COOKIE):
    """Delete cache key for this request path and page version."""
    cache_key = get_cache_key(request_path, page_version,
                                cookie_name=cookie_name)
    nginx_cache.delete(cache_key)
